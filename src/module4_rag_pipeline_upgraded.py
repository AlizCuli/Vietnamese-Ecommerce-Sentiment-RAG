"""Professional evidence-grounded RAG answer formatting.

The generator is deterministic and template-based. It does not call an LLM,
so the demo is stable offline and only summarizes retrieved review evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd

from module4_retrieve_upgraded import UpgradedReviewRetriever, resolve_project_dir

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ISSUE_RULES = {
    "Giao hàng chậm hoặc xử lý đơn lâu": [
        "giao hàng chậm",
        "giao chậm",
        "giao lâu",
        "chậm trễ",
        "giao trễ",
        "quá chậm",
        "delay",
        "đóng hàng lâu",
        "mãi chưa",
        "quá lâu",
    ],
    "Giao thiếu hàng hoặc thiếu phụ kiện": [
        "thiếu hàng",
        "giao thiếu",
        "thiếu sản phẩm",
        "thiếu phụ kiện",
        "không đủ",
    ],
    "Giao sai mẫu, sai màu hoặc sai kích cỡ": [
        "giao sai",
        "giao nhầm",
        "sai mẫu",
        "sai màu",
        "sai size",
        "không đúng mẫu",
        "không giống",
        "không như hình",
    ],
    "Sản phẩm lỗi, hỏng hoặc không hoạt động đúng": [
        "bị lỗi",
        "hàng lỗi",
        "sản phẩm lỗi",
        "hỏng",
        "hư",
        "không hoạt động",
        "không chỉnh",
        "bị hư",
    ],
    "Chất lượng kém hoặc không như mô tả": [
        "chất lượng kém",
        "quá kém",
        "kém chất lượng",
        "tệ",
        "thất vọng",
        "không như mô tả",
        "không giống hình",
    ],
    "Đóng gói hoặc bao bì có vấn đề": [
        "đóng gói",
        "bao bì",
        "móp méo",
        "móp",
        "bể",
        "vỡ",
        "không chống sốc",
        "hộp",
    ],
    "Size hoặc kích thước không phù hợp": [
        "size",
        "kích thước",
        "không vừa",
        "chật",
        "rộng",
        "cỡ",
    ],
    "Shop phản hồi hoặc hỗ trợ chưa tốt": [
        "không phản hồi",
        "không trả lời",
        "nhắn tin",
        "hỗ trợ",
        "tư vấn",
        "rep",
        "đổi trả",
        "hoàn tiền",
    ],
    "Giá cả hoặc độ đáng tiền": [
        "giá",
        "đáng tiền",
        "rẻ",
        "đắt",
        "không xứng",
    ],
}

QUERY_ASPECT_GROUPS = {
    "delivery": [
        "Giao hàng chậm hoặc xử lý đơn lâu",
        "Giao thiếu hàng hoặc thiếu phụ kiện",
        "Giao sai mẫu, sai màu hoặc sai kích cỡ",
        "Shop phản hồi hoặc hỗ trợ chưa tốt",
    ],
    "quality": [
        "Sản phẩm lỗi, hỏng hoặc không hoạt động đúng",
        "Chất lượng kém hoặc không như mô tả",
        "Giao sai mẫu, sai màu hoặc sai kích cỡ",
    ],
    "packaging": [
        "Đóng gói hoặc bao bì có vấn đề",
        "Sản phẩm lỗi, hỏng hoặc không hoạt động đúng",
    ],
    "size": [
        "Size hoặc kích thước không phù hợp",
        "Giao sai mẫu, sai màu hoặc sai kích cỡ",
        "Chất lượng kém hoặc không như mô tả",
    ],
    "service": [
        "Shop phản hồi hoặc hỗ trợ chưa tốt",
        "Giao hàng chậm hoặc xử lý đơn lâu",
    ],
    "price": [
        "Giá cả hoặc độ đáng tiền",
        "Chất lượng kém hoặc không như mô tả",
    ],
}


def normalize_for_match(text: object) -> str:
    value = unicodedata.normalize("NFD", str(text or "")).lower()
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def clean_excerpt(text: object, max_chars: int = 230) -> str:
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def infer_query_aspect(query: str) -> str | None:
    normalized = normalize_for_match(query)
    if any(term in normalized for term in ["giao", "ship", "van chuyen", "nhan hang", "cham", "tre"]):
        return "delivery"
    if any(term in normalized for term in ["loi", "hong", "hu", "chat luong", "kem chat luong", "khong dung duoc"]):
        return "quality"
    if any(term in normalized for term in ["dong goi", "bao bi", "hop", "seal", "be", "vo", "mop"]):
        return "packaging"
    if any(term in normalized for term in ["size", "kich thuoc", "rong", "chat", "khong vua", "co ao", "co giay"]):
        return "size"
    if any(term in normalized for term in ["shop", "phan hoi", "tu van", "ho tro", "rep", "tra loi"]):
        return "service"
    if any(term in normalized for term in ["gia", "dang tien", "re", "dat"]):
        return "price"
    return None


def selected_issue_rules(query: str) -> dict[str, list[str]]:
    aspect = infer_query_aspect(query)
    if not aspect:
        return ISSUE_RULES
    allowed = set(QUERY_ASPECT_GROUPS[aspect])
    return {issue: keywords for issue, keywords in ISSUE_RULES.items() if issue in allowed}


def detect_issues(query: str, evidence: pd.DataFrame) -> list[dict[str, object]]:
    comments = evidence["comment"].fillna("").astype(str).map(normalize_for_match).tolist()
    issues: list[dict[str, object]] = []
    for issue, keywords in selected_issue_rules(query).items():
        normalized_keywords = [normalize_for_match(keyword) for keyword in keywords]
        citations: list[str] = []
        for idx, comment in enumerate(comments, start=1):
            if any(keyword and keyword in comment for keyword in normalized_keywords):
                citations.append(f"[{idx}]")
        if citations:
            # Giữ citation gọn: mỗi ý chính chỉ cần 2-3 dẫn chứng tiêu biểu.
            issues.append({"issue": issue, "count": len(citations), "citations": citations[:3]})
    return sorted(issues, key=lambda item: int(item["count"]), reverse=True)


def build_evidence_items(evidence: pd.DataFrame) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for idx, (_, row) in enumerate(evidence.reset_index(drop=True).iterrows(), start=1):
        score = row.get("rerank_score", row.get("score"))
        dense_score = row.get("dense_score", row.get("score"))
        items.append(
            {
                "citation": f"[{idx}]",
                "rank": int(row.get("rank", idx)),
                "score": float(score) if pd.notna(score) else None,
                "dense_score": float(dense_score) if pd.notna(dense_score) else None,
                "category": row.get("category"),
                "product_name": row.get("product_name"),
                "rating": None if pd.isna(row.get("rating")) else row.get("rating"),
                "sentiment": row.get("predicted_sentiment"),
                "comment": str(row.get("comment", "")),
                "excerpt": clean_excerpt(row.get("comment", "")),
                "doc_id": row.get("doc_id"),
            }
        )
    return items


def estimate_confidence(evidence: pd.DataFrame, issues: list[dict[str, object]]) -> dict[str, object]:
    evidence_count = int(len(evidence))
    scores = pd.to_numeric(evidence.get("score", pd.Series(dtype=float)), errors="coerce")
    avg_score = float(scores.mean()) if len(scores) and pd.notna(scores.mean()) else None
    issue_hits = sum(int(issue["count"]) for issue in issues)

    if evidence_count == 0:
        level = "none"
        label = "Không có bằng chứng"
        warning = "Không tìm thấy review phù hợp."
    elif issue_hits >= 4 and evidence_count >= 5:
        level = "high"
        label = "Cao"
        warning = ""
    elif issue_hits >= 2:
        level = "medium"
        label = "Trung bình"
        warning = "Một số review liên quan rõ, nhưng vẫn nên đọc evidence trước khi kết luận."
    else:
        level = "low"
        label = "Thấp"
        warning = "Chưa đủ bằng chứng rõ ràng từ các review được truy xuất."

    return {
        "level": level,
        "label": label,
        "evidence_count": evidence_count,
        "issue_hits": int(issue_hits),
        "average_score": avg_score,
        "warning": warning,
    }


def build_answer_text(
    query: str,
    summary: str,
    issues: list[dict[str, object]],
    evidence_items: list[dict[str, object]],
    confidence: dict[str, object],
) -> str:
    lines = [
        "# Câu trả lời",
        "",
        "## Tóm tắt",
        summary,
        "",
        "## Các vấn đề chính",
    ]

    if issues:
        for idx, issue in enumerate(issues[:4], start=1):
            citations = "".join(issue["citations"][:3])
            lines.append(f"{idx}. {issue['issue']} {citations}.")
    else:
        lines.append("Chưa đủ bằng chứng rõ ràng từ các review được truy xuất.")

    lines.extend(["", "## Bằng chứng tiêu biểu"])
    if evidence_items:
        for item in evidence_items[:3]:
            lines.append(
                f"{item['citation']} Rating {item['rating']}, sentiment {item['sentiment']}: "
                f"\"{item['excerpt']}\""
            )
    else:
        lines.append("Không có review bằng chứng.")

    lines.extend(
        [
            "",
            "## Độ tin cậy",
            f"- Evidence liên quan: {confidence['label']}",
            f"- Số review được dùng: {confidence['evidence_count']}",
            "- Lưu ý: Câu trả lời chỉ dựa trên review truy xuất, không suy diễn ngoài dữ liệu.",
        ]
    )
    if confidence.get("warning"):
        lines.append(f"- Cảnh báo: {confidence['warning']}")
    return "\n".join(lines)


def generate_answer(query: str, evidence: pd.DataFrame) -> dict[str, Any]:
    evidence = evidence.copy().reset_index(drop=True)
    evidence_items = build_evidence_items(evidence)
    issues = detect_issues(query, evidence)
    confidence = estimate_confidence(evidence, issues)

    sentiment_counts = (
        evidence["predicted_sentiment"].fillna("unknown").astype(str).value_counts().to_dict()
        if "predicted_sentiment" in evidence.columns
        else {}
    )
    category_counts = (
        evidence["category"].fillna("unknown").astype(str).value_counts().to_dict()
        if "category" in evidence.columns
        else {}
    )

    if evidence.empty:
        summary = "Chưa tìm được review phù hợp để trả lời. Hãy thử câu hỏi cụ thể hơn hoặc bỏ bớt bộ lọc."
        issues = []
    elif issues:
        top_issue_names = [issue["issue"].lower() for issue in issues[:3]]
        summary = (
            "Trong các review được truy xuất, các phản hồi liên quan tập trung vào "
            + ", ".join(top_issue_names)
            + "."
        )
    else:
        summary = "Có review được truy xuất, nhưng mức liên quan chưa đủ rõ để kết luận chắc chắn."

    answer = build_answer_text(query, summary, issues, evidence_items, confidence)
    return {
        "query": query,
        "answer": answer,
        "summary": summary,
        "main_issues": issues[:5],
        "evidence": evidence_items,
        "confidence": confidence,
        "sentiment_distribution": sentiment_counts,
        "category_distribution": category_counts,
    }


def run_rag(
    query: str,
    top_k: int = 5,
    project_dir: str | Path | None = None,
    index_dir: str | Path = "models/module4",
    category: str | None = None,
    sentiment: str | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    exclude_app: bool | None = None,
    auto_filter: bool = True,
) -> dict[str, Any]:
    retriever = UpgradedReviewRetriever(project_dir=project_dir, index_dir=index_dir)
    evidence = retriever.retrieve(
        query=query,
        top_k=top_k,
        category=category,
        sentiment=sentiment,
        min_rating=min_rating,
        max_rating=max_rating,
        exclude_app=exclude_app,
        auto_filter=auto_filter,
    )
    output = generate_answer(query, evidence)
    output["diagnostics"] = retriever.diagnostics_dict()
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run upgraded RAG answer generation.")
    parser.add_argument("--project_dir", default=None)
    parser.add_argument("--index_dir", default="models/module4")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--category", default=None)
    parser.add_argument("--sentiment", default=None)
    parser.add_argument("--min_rating", type=float, default=None)
    parser.add_argument("--max_rating", type=float, default=None)
    parser.add_argument("--exclude_app", action="store_true")
    parser.add_argument("--no_auto_filter", action="store_true")
    parser.add_argument("--output", default="results/module4/rag_outputs_upgraded.json")
    args = parser.parse_args()

    project_dir = resolve_project_dir(args.project_dir)
    result = run_rag(
        query=args.query,
        top_k=args.top_k,
        project_dir=project_dir,
        index_dir=args.index_dir,
        category=args.category,
        sentiment=args.sentiment,
        min_rating=args.min_rating,
        max_rating=args.max_rating,
        exclude_app=args.exclude_app,
        auto_filter=not args.no_auto_filter,
    )

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = project_dir / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(result["answer"])
    print(f"\n[rag-upgraded] Saved: {output_path}")


if __name__ == "__main__":
    main()
