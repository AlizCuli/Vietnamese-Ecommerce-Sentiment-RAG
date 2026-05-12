"""FastAPI backend for the upgraded RAG web demo."""

from __future__ import annotations

import math
import sys
import time
import warnings
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

PROJECT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_DIR / "src"
FRONTEND_DIR = PROJECT_DIR / "frontend"
MODULE2_DIR = PROJECT_DIR / "models" / "module2"
MODULE4_DIR = PROJECT_DIR / "models" / "module4"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from module4_rag_pipeline_upgraded import generate_answer  # noqa: E402
from module4_retrieve_upgraded import UpgradedReviewRetriever  # noqa: E402


class RagRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)
    sentiment: str | None = None
    category: str | None = None
    rating_filter: str = "all"
    min_rating: float | None = None
    max_rating: float | None = None
    exclude_app: bool | None = None
    auto_filter: bool = True
    smart_category: bool = True
    evidence_only: bool = True
    sentiment_source: str | None = None


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1)


def safe_json(value: Any) -> Any:
    """Convert pandas/numpy values into JSON-safe Python primitives."""
    if isinstance(value, dict):
        return {str(k): safe_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [safe_json(v) for v in value]
    if isinstance(value, tuple):
        return [safe_json(v) for v in value]
    if isinstance(value, float) and math.isnan(value):
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if hasattr(value, "item"):
        try:
            return safe_json(value.item())
        except Exception:
            pass
    return value


def normalize_query(text: str) -> str:
    return str(text or "").strip().lower()


def sentiment_label_vi(label: str | None) -> str:
    labels = {
        "negative": "Tiêu cực",
        "neutral": "Trung lập",
        "positive": "Tích cực",
    }
    return labels.get(str(label or "").lower(), str(label or "Không rõ"))


def strip_vietnamese_accents(text: str) -> str:
    import unicodedata

    value = unicodedata.normalize("NFD", str(text or ""))
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return value.lower()


def infer_query_aspect(query: str) -> dict[str, Any]:
    normalized = strip_vietnamese_accents(query)
    aspect_rules = [
        ("Giao hàng", ["giao hang", "ship", "van chuyen", "giao cham", "giao lau", "nhan hang"]),
        ("Sai hàng", ["sai hang", "giao sai", "giao nham", "khong dung mau", "sai mau"]),
        ("Thiếu hàng", ["thieu hang", "thieu phu kien", "khong du", "giao thieu"]),
        ("Đóng gói", ["dong goi", "bao bi", "hop", "seal", "mop", "be", "vo"]),
        ("Chất lượng", ["chat luong", "kem", "khong nhu mo ta", "khong giong", "te"]),
        ("Hàng lỗi/hỏng", ["loi", "hong", "hu", "khong hoat dong", "bi loi"]),
        ("Size/kích thước", ["size", "kich thuoc", "khong vua", "chat", "rong"]),
        ("Shop hỗ trợ", ["shop", "phan hoi", "tu van", "ho tro", "rep", "tra loi"]),
        ("Giá cả", ["gia", "dang tien", "re", "dat"]),
    ]
    for label, keywords in aspect_rules:
        if any(keyword in normalized for keyword in keywords):
            return {"label": label, "keywords": keywords}
    return {"label": "Tổng quát", "keywords": []}


def build_filter_reason(request: RagRequest, filters: dict[str, Any], aspect: dict[str, Any]) -> str:
    if not request.auto_filter:
        return "Auto filter đang tắt, hệ thống chỉ dùng các bộ lọc người dùng chọn."

    normalized = strip_vietnamese_accents(request.query)
    reasons: list[str] = []
    if any(term in normalized for term in ["phan nan", "che", "loi", "hong", "kem", "te", "cham", "sai", "thieu"]):
        reasons.append("câu hỏi có dấu hiệu tìm phản hồi tiêu cực")
    if aspect["label"] != "Tổng quát":
        reasons.append(f"hệ thống nhận diện chủ đề {aspect['label'].lower()}")
    if filters.get("category"):
        reasons.append(f"áp dụng ngành hàng {filters['category']}")
    if filters.get("exclude_app"):
        reasons.append("loại category App để ưu tiên review sản phẩm vật lý")

    return "; ".join(reasons) if reasons else "Không áp dụng filter ngầm ngoài cấu hình mặc định."


def build_query_understanding(
    request: RagRequest,
    filters: dict[str, Any],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    aspect = infer_query_aspect(request.query)
    expanded_query = str(diagnostics.get("expanded_query") or request.query)
    original_query = str(request.query)
    applied_sentiment = filters.get("sentiment") or diagnostics.get("sentiment_filter")
    applied_category = filters.get("category") or diagnostics.get("category_filter")
    expansion_terms = [
        term.strip()
        for term in expanded_query.replace(original_query, "", 1).split()
        if term.strip()
    ]
    return {
        "answered_query": request.query,
        "aspect": aspect["label"],
        "aspect_keywords": aspect["keywords"][:8],
        "sentiment_filter": sentiment_label_vi(applied_sentiment) if applied_sentiment else "Tất cả",
        "category_filter": applied_category or "Tất cả",
        "rating_filter": request.rating_filter,
        "expanded_query": expanded_query,
        "expansion_terms": expansion_terms[:16],
        "top_k": request.top_k,
        "auto_filter": request.auto_filter,
        "filter_reason": build_filter_reason(request, filters, aspect),
    }


def load_precision_at_5() -> dict[str, Any]:
    """Read Precision@5 and label it as current or baseline.

    The old submission stores manual Precision@5 in module5; that number is a
    baseline unless the upgraded experiment exports a new precision summary.
    """
    candidates = [
        (
            PROJECT_DIR / "results" / "module4" / "precision_at_k_summary.csv",
            "current",
            "Precision@5 hiện tại",
        ),
        (
            PROJECT_DIR / "results" / "module5" / "manual_precision_overall.csv",
            "baseline",
            "Precision@5 baseline",
        ),
    ]
    for path, source, label in candidates:
        if not path.exists():
            continue
        try:
            df = pd.read_csv(path)
            if "k" in df.columns and "average_precision_at_k" in df.columns:
                row = df[df["k"].astype(str) == "5"]
                if not row.empty:
                    return {
                        "value": float(row.iloc[0]["average_precision_at_k"]),
                        "source": source,
                        "label": label,
                        "file": str(path.relative_to(PROJECT_DIR)),
                    }
            if "precision@5" in df.columns:
                return {
                    "value": float(pd.to_numeric(df["precision@5"], errors="coerce").dropna().mean()),
                    "source": source,
                    "label": label,
                    "file": str(path.relative_to(PROJECT_DIR)),
                }
        except Exception:
            continue
    return {"value": None, "source": "missing", "label": "Precision@5", "file": None}


def infer_filters_from_query(request: RagRequest) -> dict[str, Any]:
    """Infer safe UI filters without hiding user-selected filters."""
    query = normalize_query(request.query)

    sentiment = request.sentiment
    if sentiment in {"", "auto", "__auto__"}:
        sentiment = None
    if sentiment in {"all", "__all__"}:
        sentiment = None
        auto_filter = False
    else:
        auto_filter = request.auto_filter

    category = request.category or None
    if category in {"", "all", "__all__"}:
        category = None

    if request.smart_category and not category:
        if any(term in query for term in ["size", "kích thước", "rong", "rộng", "chật", "không vừa", "khong vua"]):
            category = "Fashion"

    min_rating = request.min_rating
    max_rating = request.max_rating
    if request.rating_filter == "low":
        min_rating, max_rating = 1, 2
    elif request.rating_filter == "mid":
        min_rating, max_rating = 3, 3
    elif request.rating_filter == "high":
        min_rating, max_rating = 4, 5

    exclude_app = request.exclude_app
    if exclude_app is None and request.smart_category:
        product_terms = [
            "sản phẩm",
            "san pham",
            "hàng",
            "hang",
            "chất lượng",
            "chat luong",
            "giao hàng",
            "giao hang",
            "đóng gói",
            "dong goi",
            "size",
            "bao bì",
            "bao bi",
        ]
        exclude_app = any(term in query for term in product_terms)

    return {
        "sentiment": sentiment,
        "category": category,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "exclude_app": exclude_app,
        "auto_filter": auto_filter,
    }


@lru_cache(maxsize=1)
def load_resources() -> UpgradedReviewRetriever:
    """Load FAISS, metadata and embedding model once for the web process."""
    return UpgradedReviewRetriever(project_dir=PROJECT_DIR, index_dir="models/module4")


@lru_cache(maxsize=1)
def load_sentiment_model() -> tuple[Any, Path]:
    """Load the Module 2 sentiment classifier once for live demo inference."""
    candidates = [
        MODULE2_DIR / "best_model.joblib",
        MODULE2_DIR / "tfidf_linearsvm.joblib",
        MODULE2_DIR / "tfidf_logreg.joblib",
    ]
    for path in candidates:
        if path.exists():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return joblib.load(path), path
    raise FileNotFoundError("Không tìm thấy sentiment model trong models/module2/.")


def predict_sentiment(text: str) -> dict[str, Any]:
    """Predict sentiment for one review using the trained Module 2 model."""
    model, model_path = load_sentiment_model()
    clean_text = str(text or "").strip()
    if not clean_text:
        raise ValueError("Vui lòng nhập review để phân tích sentiment.")

    label = str(model.predict([clean_text])[0])
    result: dict[str, Any] = {
        "label": label,
        "label_vi": sentiment_label_vi(label),
        "model_path": str(model_path.relative_to(PROJECT_DIR)),
        "confidence": None,
        "margin": None,
        "scores": {},
    }

    classes = [str(item) for item in getattr(model, "classes_", [])]
    if hasattr(model, "decision_function"):
        scores = model.decision_function([clean_text])
        values = scores[0] if getattr(scores, "ndim", 1) > 1 else scores
        score_map = {classes[idx]: float(value) for idx, value in enumerate(values)} if classes else {}
        sorted_scores = sorted(score_map.values(), reverse=True)
        result["scores"] = score_map
        if sorted_scores:
            result["confidence"] = float(sorted_scores[0])
        if len(sorted_scores) >= 2:
            result["margin"] = float(sorted_scores[0] - sorted_scores[1])
    elif hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([clean_text])[0]
        score_map = {classes[idx]: float(value) for idx, value in enumerate(probabilities)} if classes else {}
        sorted_scores = sorted(score_map.values(), reverse=True)
        result["scores"] = score_map
        if sorted_scores:
            result["confidence"] = float(sorted_scores[0])
        if len(sorted_scores) >= 2:
            result["margin"] = float(sorted_scores[0] - sorted_scores[1])

    return result


def run_retrieval(request: RagRequest) -> dict[str, Any]:
    filters = infer_filters_from_query(request)
    retriever = load_resources()
    evidence = retriever.retrieve(
        query=request.query,
        top_k=request.top_k,
        category=filters["category"],
        sentiment=filters["sentiment"],
        min_rating=filters["min_rating"],
        max_rating=filters["max_rating"],
        exclude_app=filters["exclude_app"],
        auto_filter=filters["auto_filter"],
    )
    return {"retriever": retriever, "evidence": evidence, "filters": filters}


def build_technical_details(
    request: RagRequest,
    retriever: UpgradedReviewRetriever,
    filters: dict[str, Any],
    elapsed_ms: float,
) -> dict[str, Any]:
    diagnostics = retriever.diagnostics_dict()
    diagnostics.update(
        {
            "original_query": request.query,
            "top_k": request.top_k,
            "filters_applied": filters,
            "sentiment_source": request.sentiment_source or "auto/manual",
            "embedding_model": retriever.model_name,
            "faiss_index_path": "models/module4/review_faiss.index",
            "metadata_path": "models/module4/review_metadata.parquet",
            "retrieval_time_ms": round(elapsed_ms, 2),
        }
    )
    return diagnostics


app = FastAPI(
    title="Vietnamese E-commerce Sentiment + RAG Demo",
    version="1.1.0",
    description="Backend API for evidence-grounded RAG over Vietnamese e-commerce reviews.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "project_dir": str(PROJECT_DIR),
        "index_exists": (MODULE4_DIR / "review_faiss.index").exists(),
        "metadata_exists": (MODULE4_DIR / "review_metadata.parquet").exists(),
        "config_exists": (MODULE4_DIR / "module4_index_config.json").exists(),
        "sentiment_model_exists": (MODULE2_DIR / "best_model.joblib").exists(),
    }


@app.get("/api/config")
def config() -> dict[str, Any]:
    try:
        retriever = load_resources()
        categories = retriever.metadata["category"].fillna("").astype(str).replace("", "unknown").value_counts().head(30)
        sentiments = retriever.metadata["predicted_sentiment"].fillna("").astype(str).replace("", "unknown").value_counts()
        precision = load_precision_at_5()
        return safe_json(
            {
                "num_documents": int(retriever.index.ntotal),
                "embedding_model": retriever.model_name,
                "retrieval_method": "Dense FAISS + query expansion + lightweight rerank",
                "sentiment_model": (
                    str((MODULE2_DIR / "best_model.joblib").relative_to(PROJECT_DIR))
                    if (MODULE2_DIR / "best_model.joblib").exists()
                    else None
                ),
                "precision_at_5": precision["value"],
                "precision_label": precision["label"],
                "precision_source": precision["source"],
                "precision_file": precision["file"],
                "resource_cache": "model/index đã cache trong backend",
                "categories": categories.to_dict(),
                "sentiments": sentiments.to_dict(),
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Không load được RAG resources: {exc}") from exc


@app.post("/api/sentiment")
def sentiment(request: SentimentRequest) -> dict[str, Any]:
    try:
        return safe_json(predict_sentiment(request.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Không chạy được sentiment model: {exc}") from exc


@app.post("/api/rag")
def rag(request: RagRequest) -> dict[str, Any]:
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập câu hỏi RAG.")

    start = time.perf_counter()
    try:
        result_bundle = run_retrieval(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        retriever = result_bundle["retriever"]
        evidence = result_bundle["evidence"]
        filters = result_bundle["filters"]

        result = generate_answer(request.query, evidence)
        diagnostics = build_technical_details(request, retriever, filters, elapsed_ms)
        result["diagnostics"] = diagnostics
        result["understanding"] = build_query_understanding(request, filters, diagnostics)
        result["status"] = "no_results" if len(evidence) == 0 else "success"
        return safe_json(result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Không chạy được RAG: {exc}") from exc


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
