"""Upgraded retrieval utilities for Module 4 RAG.

This file is intentionally additive. It does not replace module4_retrieve.py.
The web demo and upgraded RAG pipeline import this module so the original
submission can still run unchanged.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


OUTPUT_COLUMNS = [
    "rank",
    "score",
    "dense_score",
    "keyword_score",
    "aspect_score",
    "rerank_score",
    "doc_id",
    "category",
    "product_name",
    "product_id",
    "rating",
    "predicted_sentiment",
    "sentiment_confidence",
    "comment",
    "retrieval_text",
]


QUERY_EXPANSIONS = {
    "giao hàng": ["ship", "vận chuyển", "nhận hàng", "đóng hàng", "gửi hàng"],
    "chậm": ["lâu", "trễ", "delay", "mãi chưa nhận", "quá lâu"],
    "thiếu": ["thiếu hàng", "thiếu sản phẩm", "thiếu phụ kiện", "không đủ"],
    "sai": ["giao sai", "giao nhầm", "không đúng mẫu", "sai màu", "sai size"],
    "lỗi": ["hỏng", "hư", "không hoạt động", "bị lỗi", "defect"],
    "đóng gói": ["bao bì", "gói hàng", "hộp", "seal", "chống sốc", "móp méo"],
    "shop": ["tư vấn", "hỗ trợ", "rep", "trả lời", "phản hồi"],
    "size": ["kích thước", "không vừa", "chật", "rộng", "cỡ"],
    "chất lượng": ["hàng kém", "không giống hình", "không như mô tả", "độ bền"],
    "giá": ["đáng tiền", "rẻ", "đắt", "giá cả"],
}


NEGATIVE_QUERY_MARKERS = [
    "phàn nàn",
    "chê",
    "tiêu cực",
    "không hài lòng",
    "vấn đề",
    "lỗi",
    "hỏng",
    "hư",
    "chậm",
    "thiếu",
    "sai",
    "kém",
    "tệ",
    "móp",
    "vỡ",
]


PHYSICAL_PRODUCT_MARKERS = [
    "sản phẩm",
    "hàng",
    "chất lượng",
    "đóng gói",
    "bao bì",
    "giao hàng",
    "size",
    "kích thước",
    "màu",
    "mẫu",
    "quần",
    "áo",
    "giày",
    "đồng hồ",
]


ASPECT_KEYWORDS = {
    "giao hàng chậm": ["giao hàng chậm", "giao chậm", "giao lâu", "chậm trễ", "giao trễ", "đóng hàng lâu"],
    "giao thiếu hàng": ["thiếu hàng", "giao thiếu", "thiếu sản phẩm", "thiếu phụ kiện", "không đủ"],
    "giao sai hàng": ["giao sai", "giao nhầm", "sai hàng", "không đúng mẫu", "sai màu", "sai size"],
    "sản phẩm lỗi/hỏng": ["bị lỗi", "hàng lỗi", "hỏng", "hư", "không hoạt động", "không chỉnh"],
    "chất lượng kém": ["chất lượng kém", "quá kém", "tệ", "thất vọng", "không giống hình", "không như mô tả"],
    "đóng gói kém": ["đóng gói", "bao bì", "móp méo", "bể", "vỡ", "không chống sốc"],
    "size không vừa": ["size", "kích thước", "không vừa", "chật", "rộng", "cỡ"],
    "shop phản hồi kém": ["không phản hồi", "không trả lời", "nhắn tin", "hỗ trợ", "tư vấn"],
    "giá cả": ["giá", "đáng tiền", "rẻ", "đắt"],
}


def resolve_project_dir(project_dir: str | None = None) -> Path:
    if project_dir:
        return Path(project_dir).expanduser().resolve()
    env_dir = os.environ.get("PROJECT_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def resolve_path(project_dir: Path, path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else project_dir / path


def normalize_text(text: object) -> str:
    value = unicodedata.normalize("NFC", str(text or "")).lower()
    value = re.sub(r"\s+", " ", value).strip()
    return value


def strip_accents(text: object) -> str:
    value = unicodedata.normalize("NFD", str(text or ""))
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower()
    value = re.sub(r"\s+", " ", value).strip()
    return value


def contains_any(text: object, markers: list[str]) -> bool:
    normalized = normalize_text(text)
    no_accent = strip_accents(text)
    return any(normalize_text(marker) in normalized or strip_accents(marker) in no_accent for marker in markers)


def expand_vietnamese_query(query: str) -> str:
    """Rule-based query expansion for common Vietnamese e-commerce complaints."""
    parts = [str(query).strip()]
    normalized = normalize_text(query)
    for key, synonyms in QUERY_EXPANSIONS.items():
        if normalize_text(key) in normalized:
            parts.extend(synonyms)
    deduped = list(dict.fromkeys([part for part in parts if part]))
    return " ".join(deduped)


def infer_default_sentiment(query: str, sentiment: str | None = None) -> str | None:
    if sentiment:
        return sentiment
    if contains_any(query, NEGATIVE_QUERY_MARKERS):
        return "negative"
    return None


def should_exclude_app(query: str, exclude_app: bool | None = None) -> bool:
    if exclude_app is not None:
        return bool(exclude_app)
    return contains_any(query, PHYSICAL_PRODUCT_MARKERS)


def infer_query_aspect_keywords(query: str) -> list[str]:
    normalized = normalize_text(query)
    no_accent = strip_accents(query)
    selected: list[str] = []
    for keywords in ASPECT_KEYWORDS.values():
        if any(normalize_text(keyword) in normalized or strip_accents(keyword) in no_accent for keyword in keywords):
            selected.extend(keywords)
    if selected:
        return list(dict.fromkeys(selected))

    query_terms = [term for term in re.split(r"\W+", no_accent) if len(term) >= 3]
    return query_terms[:12]


def minmax_scale(values: pd.Series) -> pd.Series:
    values = pd.to_numeric(values, errors="coerce").fillna(0.0)
    min_value = float(values.min())
    max_value = float(values.max())
    if max_value <= min_value:
        return pd.Series(np.zeros(len(values)), index=values.index)
    return (values - min_value) / (max_value - min_value)


@dataclass
class RetrievalDiagnostics:
    expanded_query: str
    sentiment_filter: str | None
    category_filter: str | None
    exclude_app: bool
    candidate_k: int
    returned_rows: int


class UpgradedReviewRetriever:
    """FAISS retriever with query expansion, metadata filters and light reranking."""

    def __init__(
        self,
        project_dir: str | Path | None = None,
        index_dir: str | Path = "models/module4",
        model_name: str | None = None,
    ) -> None:
        self.project_dir = resolve_project_dir(str(project_dir)) if project_dir else resolve_project_dir()
        self.index_dir = resolve_path(self.project_dir, index_dir)
        self.index_path = self.index_dir / "review_faiss.index"
        self.metadata_path = self.index_dir / "review_metadata.parquet"
        self.config_path = self.index_dir / "module4_index_config.json"

        if not self.index_path.exists():
            raise FileNotFoundError(f"FAISS index not found: {self.index_path}")
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata parquet not found: {self.metadata_path}")
        if not self.config_path.exists():
            raise FileNotFoundError(f"Index config not found: {self.config_path}")

        try:
            import faiss
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "Missing Module 4 dependencies. Run: pip install -q -r requirements_module4.txt"
            ) from exc

        self.faiss = faiss
        self.config: dict[str, Any] = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.model_name = model_name or self.config.get("embedding_model", "intfloat/multilingual-e5-small")
        self.query_prefix = self.config.get("e5_query_prefix", "query: ")

        print(f"[rag-upgraded] Loading FAISS index: {self.index_path}")
        self.index = self._read_faiss_index(self.index_path)
        self.metadata = pd.read_parquet(self.metadata_path).reset_index(drop=True)
        self.metadata = self._normalize_metadata(self.metadata)

        print(f"[rag-upgraded] Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)

        if self.index.ntotal != len(self.metadata):
            raise AssertionError(
                f"index.ntotal={self.index.ntotal} != metadata rows={len(self.metadata)}"
            )

    def _read_faiss_index(self, path: Path):
        """Read FAISS index robustly on Windows paths containing Vietnamese text."""
        try:
            return self.faiss.read_index(str(path))
        except RuntimeError:
            # Some FAISS Windows builds cannot open non-ASCII paths. Reading the
            # file as bytes and deserializing avoids passing the path to FAISS.
            raw = path.read_bytes()
            buffer = np.frombuffer(raw, dtype="uint8")
            return self.faiss.deserialize_index(buffer)

    @staticmethod
    def _normalize_metadata(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for column in ["comment", "retrieval_text", "category", "product_name", "predicted_sentiment"]:
            if column not in df.columns:
                df[column] = ""
            df[column] = df[column].fillna("").astype(str)

        if "rating" in df.columns:
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        else:
            df["rating"] = np.nan

        if "product_id" not in df.columns:
            df["product_id"] = ""
        if "doc_id" not in df.columns:
            df["doc_id"] = np.arange(len(df)).astype(str)
        if "sentiment_confidence" not in df.columns:
            df["sentiment_confidence"] = np.nan
        return df

    def _embed_query(self, query: str) -> np.ndarray:
        if not query or not str(query).strip():
            raise ValueError("query must be non-empty")
        query_text = self.query_prefix + str(query).strip()
        embedding = self.model.encode(
            [query_text],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.ascontiguousarray(embedding.astype("float32"))

    @staticmethod
    def _apply_filters(
        df: pd.DataFrame,
        category: str | None = None,
        sentiment: str | None = None,
        min_rating: float | None = None,
        max_rating: float | None = None,
        product_id: str | None = None,
        product_name_contains: str | None = None,
        exclude_app: bool = False,
    ) -> pd.DataFrame:
        filtered = df
        if category:
            filtered = filtered[
                filtered["category"].fillna("").astype(str).str.lower() == category.lower()
            ]
        if sentiment:
            filtered = filtered[
                filtered["predicted_sentiment"].fillna("").astype(str).str.lower() == sentiment.lower()
            ]
        if exclude_app:
            filtered = filtered[
                filtered["category"].fillna("").astype(str).str.lower() != "app"
            ]
        if min_rating is not None:
            rating = pd.to_numeric(filtered["rating"], errors="coerce")
            filtered = filtered[rating >= min_rating]
        if max_rating is not None:
            rating = pd.to_numeric(filtered["rating"], errors="coerce")
            filtered = filtered[rating <= max_rating]
        if product_id:
            filtered = filtered[
                filtered["product_id"].fillna("").astype(str).str.lower() == product_id.lower()
            ]
        if product_name_contains:
            filtered = filtered[
                filtered["product_name"]
                .fillna("")
                .astype(str)
                .str.contains(product_name_contains, case=False, regex=False)
            ]
        return filtered

    @staticmethod
    def _score_keywords(df: pd.DataFrame, aspect_keywords: list[str]) -> pd.Series:
        if not aspect_keywords:
            return pd.Series(np.zeros(len(df)), index=df.index)
        text = (
            df["comment"].fillna("").astype(str)
            + " "
            + df["product_name"].fillna("").astype(str)
            + " "
            + df["retrieval_text"].fillna("").astype(str)
        )
        normalized_text = text.map(strip_accents)
        normalized_keywords = [strip_accents(keyword) for keyword in aspect_keywords]
        scores = []
        for value in normalized_text:
            hit_count = sum(1 for keyword in normalized_keywords if keyword and keyword in value)
            scores.append(hit_count / max(len(normalized_keywords), 1))
        return pd.Series(scores, index=df.index).clip(0.0, 1.0)

    @staticmethod
    def _score_aspects(df: pd.DataFrame, query: str) -> pd.Series:
        query_normalized = strip_accents(query)
        text = (
            df["comment"].fillna("").astype(str)
            + " "
            + df["retrieval_text"].fillna("").astype(str)
        ).map(strip_accents)
        scores = np.zeros(len(df), dtype=float)
        for aspect, keywords in ASPECT_KEYWORDS.items():
            aspect_hit = any(strip_accents(keyword) in query_normalized for keyword in keywords)
            if not aspect_hit:
                continue
            for keyword in keywords:
                keyword_normalized = strip_accents(keyword)
                if not keyword_normalized:
                    continue
                scores += text.str.contains(re.escape(keyword_normalized), regex=True, na=False).astype(float)
        if len(scores) == 0:
            return pd.Series([], dtype=float)
        return pd.Series(scores, index=df.index).clip(0.0, 3.0) / 3.0

    @staticmethod
    def _ensure_output_columns(df: pd.DataFrame) -> pd.DataFrame:
        for column in OUTPUT_COLUMNS:
            if column not in df.columns:
                df[column] = np.nan
        return df[OUTPUT_COLUMNS]

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: str | None = None,
        sentiment: str | None = None,
        min_rating: float | None = None,
        max_rating: float | None = None,
        product_id: str | None = None,
        product_name_contains: str | None = None,
        exclude_app: bool | None = None,
        auto_filter: bool = True,
        candidate_multiplier: int = 60,
    ) -> pd.DataFrame:
        top_k = max(int(top_k), 1)
        sentiment_filter = infer_default_sentiment(query, sentiment) if auto_filter else sentiment
        exclude_app_filter = should_exclude_app(query, exclude_app) if auto_filter else bool(exclude_app)
        expanded_query = expand_vietnamese_query(query)
        aspect_keywords = infer_query_aspect_keywords(expanded_query)

        query_embedding = self._embed_query(expanded_query)
        candidate_k = min(max(top_k * candidate_multiplier, 200), int(self.index.ntotal))

        scores, indices = self.index.search(query_embedding, candidate_k)
        rows = self.metadata.iloc[indices[0]].copy().reset_index(drop=True)
        rows["dense_score"] = scores[0]
        rows["score"] = rows["dense_score"]

        filtered = self._apply_filters(
            rows,
            category=category,
            sentiment=sentiment_filter,
            min_rating=min_rating,
            max_rating=max_rating,
            product_id=product_id,
            product_name_contains=product_name_contains,
            exclude_app=exclude_app_filter,
        )

        if len(filtered) < top_k and candidate_k < self.index.ntotal:
            scores, indices = self.index.search(query_embedding, int(self.index.ntotal))
            rows = self.metadata.iloc[indices[0]].copy().reset_index(drop=True)
            rows["dense_score"] = scores[0]
            rows["score"] = rows["dense_score"]
            filtered = self._apply_filters(
                rows,
                category=category,
                sentiment=sentiment_filter,
                min_rating=min_rating,
                max_rating=max_rating,
                product_id=product_id,
                product_name_contains=product_name_contains,
                exclude_app=exclude_app_filter,
            )

        filtered = filtered.copy().reset_index(drop=True)
        filtered["keyword_score"] = self._score_keywords(filtered, aspect_keywords)
        filtered["aspect_score"] = self._score_aspects(filtered, expanded_query)
        dense_scaled = minmax_scale(filtered["dense_score"]) if len(filtered) else pd.Series(dtype=float)
        filtered["rerank_score"] = (
            0.72 * dense_scaled
            + 0.18 * filtered["keyword_score"].fillna(0.0)
            + 0.10 * filtered["aspect_score"].fillna(0.0)
        )
        filtered = filtered.sort_values(
            ["rerank_score", "dense_score"], ascending=False
        ).head(top_k).copy()
        filtered.insert(0, "rank", np.arange(1, len(filtered) + 1))

        self.last_diagnostics = RetrievalDiagnostics(
            expanded_query=expanded_query,
            sentiment_filter=sentiment_filter,
            category_filter=category,
            exclude_app=exclude_app_filter,
            candidate_k=candidate_k,
            returned_rows=int(len(filtered)),
        )
        return self._ensure_output_columns(filtered.reset_index(drop=True))

    def diagnostics_dict(self) -> dict[str, object]:
        diagnostics = getattr(self, "last_diagnostics", None)
        return diagnostics.__dict__ if diagnostics else {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run upgraded Module 4 retrieval.")
    parser.add_argument("--project_dir", default=None)
    parser.add_argument("--index_dir", default="models/module4")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--category", default=None)
    parser.add_argument("--sentiment", default=None)
    parser.add_argument("--min_rating", type=float, default=None)
    parser.add_argument("--max_rating", type=float, default=None)
    parser.add_argument("--product_id", default=None)
    parser.add_argument("--product_name_contains", default=None)
    parser.add_argument("--exclude_app", action="store_true")
    parser.add_argument("--no_auto_filter", action="store_true")
    args = parser.parse_args()

    retriever = UpgradedReviewRetriever(
        project_dir=resolve_project_dir(args.project_dir),
        index_dir=args.index_dir,
    )
    results = retriever.retrieve(
        query=args.query,
        top_k=args.top_k,
        category=args.category,
        sentiment=args.sentiment,
        min_rating=args.min_rating,
        max_rating=args.max_rating,
        product_id=args.product_id,
        product_name_contains=args.product_name_contains,
        exclude_app=args.exclude_app,
        auto_filter=not args.no_auto_filter,
    )
    print(json.dumps(retriever.diagnostics_dict(), ensure_ascii=False, indent=2))
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
