# Vietnamese E-commerce Sentiment Analysis + RAG

## Đề tài

**Ứng dụng Xử lý ngôn ngữ tự nhiên và Retrieval-Augmented Generation trong phân tích cảm xúc đánh giá sản phẩm TMĐT**

## Mục tiêu

Project xây dựng một hệ thống gồm:

1. **Sentiment Classification**: phân loại cảm xúc review sản phẩm thành Tiêu cực / Trung lập / Tích cực.
2. **RAG Review Insight**: truy xuất review liên quan đến câu hỏi và tạo câu trả lời có bằng chứng.
3. **Module 6 Hybrid Retrieval**: hướng nâng cấp retrieval bằng BM25 + Dense FAISS + RRF/rerank theo aspect.
4. **Web demo**: giao diện 3 tab để chạy sentiment, chạy RAG và xem thông tin kỹ thuật/đánh giá.

## Cách chạy nhanh

```powershell
python -m pip install -r requirements_webapp.txt
python -m pip install -r requirements_module4.txt
python scripts\run_rag_webapp.py
```

Mở:

```text
http://127.0.0.1:8000
```

## Demo nên trình bày theo thứ tự

1. Tab `Phân tích Sentiment`: nhập một review thật và dự đoán cảm xúc.
2. Tab `Hỏi đáp RAG`: hỏi về giao hàng, chất lượng, sai hàng, thiếu hàng, đóng gói.
3. Tab `Kỹ thuật & đánh giá`: trình bày corpus 82.677 review, model, FAISS index và metric.

## File nên đọc trước

- `README_DEMO.md`: hướng dẫn chạy và quay demo.
- `EXPLAIN_PROJECT_FOR_BEGINNER.md`: giải thích toàn bộ project cho người mới.
- `README_MODULE2.md`: sentiment model.
- `README_MODULE4.md`: retrieval/RAG.
- `README_MODULE6.md`: hybrid retrieval + aspect-aware reranking.
- `README_RAG_WEBAPP.md`: backend/frontend web app.

## Artifact chính

- `models/module2/best_model.joblib`: model sentiment chính.
- `models/module4/review_faiss.index`: FAISS index cho retrieval.
- `models/module4/review_metadata.parquet`: metadata review cho RAG.
- `data/processed/rag_corpus_module4.csv`: corpus RAG 82.677 documents.

## Module 6 Hybrid Retrieval

Module 6 là phần nâng cấp kỹ thuật, không thay thế web demo chính. Module này dùng:

```text
BM25 keyword search + Dense FAISS retrieval + RRF fusion + optional reranker + aspect rules
```

Chạy thử:

```powershell
python -m pip install -r requirements_module6.txt
python scripts\run_module6_hybrid_rerank_demo.py --query "Khách phàn nàn gì về giao hàng?" --top-candidates 50 --top-evidence 5 --use-reranker false --target-aspect giao_hang
```

Output:

```text
results/module6/last_hybrid_rerank_demo.json
```

## Đóng gói nộp bài

```powershell
python scripts\package_final_submission.py
```

Output:

```text
ecommerce_sentiment_rag_final_submission.zip
artifact_manifest.json
```
