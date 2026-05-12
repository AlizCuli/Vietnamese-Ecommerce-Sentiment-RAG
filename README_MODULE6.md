# README MODULE 6 - Aspect-aware Hybrid Retrieval

## Vai trò

Module 6 là phần nâng cấp kỹ thuật cho retrieval/RAG. Module này không thay thế web demo chính, mà bổ sung một pipeline thử nghiệm mạnh hơn để tìm evidence review.

Nói đơn giản: **Module 6 kết hợp tìm kiếm theo từ khóa BM25 với dense retrieval FAISS, sau đó fusion/rerank để lấy review liên quan tốt hơn.**

## Vì sao cần Module 6?

Dense retrieval ở Module 4 hiểu nghĩa tốt, nhưng đôi khi bỏ sót các cụm complaint ngắn như:

- `sai size`
- `giao sai`
- `shop không trả lời`
- `móp hộp`
- `chất lượng kém`

BM25 lại mạnh khi query và review có cùng từ khóa. Vì vậy Module 6 kết hợp cả hai hướng:

```text
BM25 keyword search + Dense FAISS retrieval -> RRF fusion -> optional reranker -> aspect sentiment evidence
```

## Thành phần chính

- `BM25`: bắt từ khóa complaint rõ ràng.
- `Dense FAISS`: tìm review gần nghĩa bằng embedding.
- `RRF fusion`: gộp ranking của BM25 và dense retrieval.
- `Optional CrossEncoder reranker`: nếu có model thì rerank, nếu không có thì fallback sang lexical rerank.
- `Aspect-aware rules`: nhận diện khía cạnh như giao hàng, đóng gói, chất lượng, dịch vụ shop, giá, size/màu.

## File code

```text
src/module6_hybrid_retrieval.py
src/module6_reranker.py
src/module6_aspect_sentiment.py
src/module6_query_intent.py
```

## Script chạy

Chạy demo một câu hỏi:

```powershell
python scripts\run_module6_hybrid_rerank_demo.py --query "Khách phàn nàn gì về giao hàng?" --top-candidates 50 --top-evidence 5 --use-reranker false --target-aspect giao_hang
```

Chạy benchmark nhỏ:

```powershell
python scripts\evaluate_module6_retrieval.py
```

Nếu muốn chạy nhanh, không load dense FAISS:

```powershell
$env:MODULE6_SKIP_DENSE="1"
python scripts\run_module6_hybrid_rerank_demo.py --query "Có vấn đề gì về đóng gói không?" --top-candidates 30 --top-evidence 5 --use-reranker false --target-aspect dong_goi
Remove-Item Env:MODULE6_SKIP_DENSE
```

## Input

Module 6 dùng lại artifact hiện có:

```text
data/processed/rag_corpus_module4.csv
models/module4/review_faiss.index
models/module4/review_metadata.parquet
models/module4/module4_index_config.json
data/eval/module6_queries.jsonl
```

Trong bản final của project này, corpus RAG có **82.677 review/documents**.

## Output

```text
results/module6/last_hybrid_rerank_demo.json
reports/module6_retrieval_eval.csv
figures/module6/module6_retrieval_comparison.png
```

Các file có hậu tố `reference` là kết quả tham khảo lấy từ project hybrid ban đầu. Khi chạy lại trên corpus 82.677 review, script sẽ tạo output mới.

## Lưu ý khi trình bày với thầy

Nên nói:

```text
Module 6 là hướng nâng cấp retrieval. Nó kết hợp BM25 và dense FAISS để cải thiện khả năng bắt các phàn nàn ngắn theo aspect.
```

Không nên nói:

```text
Module 6 là LLM hoặc chatbot sinh câu trả lời tự do.
```

Module 6 vẫn là evidence-centric retrieval, không phải full LLM RAG.

## Có cần dùng Module 6 trong video 5 phút không?

Không bắt buộc. Video chính nên tập trung:

1. Tab Sentiment.
2. Tab RAG.
3. Tab Kỹ thuật.

Nếu còn thời gian, chỉ nhắc một câu:

```text
Project còn bổ sung Module 6 như hướng nâng cấp retrieval bằng hybrid BM25 + FAISS + aspect-aware reranking.
```
