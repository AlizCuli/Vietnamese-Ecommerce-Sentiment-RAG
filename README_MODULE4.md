# README MODULE 4 - Retrieval and RAG

## Vai trò

Module 4 là phần Retrieval/RAG của đề tài. Module này tìm các review liên quan đến câu hỏi người dùng và tạo câu trả lời có bằng chứng.

Nói đơn giản: **người dùng hỏi, hệ thống tìm review thật liên quan, rồi trả lời dựa trên các review đó.**

## Input bản final

```text
data/processed/rag_corpus_module4.csv
models/module4/review_faiss.index
models/module4/review_metadata.parquet
models/module4/module4_index_config.json
```

Thông tin index:

- số documents: **82.677**
- embedding model: `intfloat/multilingual-e5-small`
- embedding dim: `384`
- index type: `FAISS IndexFlatIP`
- similarity: cosine thông qua normalized inner product

## File code gốc

```text
src/module4_prepare_inputs.py
src/module4_build_index.py
src/module4_retrieve.py
src/module4_rag_pipeline.py
src/module4_evaluate.py
```

## File code nâng cấp dùng trong demo

```text
src/module4_retrieve_upgraded.py
src/module4_rag_pipeline_upgraded.py
```

Hai file nâng cấp này giữ logic tương thích với project cũ nhưng thêm:

- query expansion tiếng Việt,
- filter theo sentiment/category/rating,
- loại category `App` nếu cần,
- lightweight rerank theo từ khóa/aspect,
- output có `Tóm tắt`, `Vấn đề chính`, `Bằng chứng`, `Độ tin cậy`.

## Retrieval là gì?

Retrieval là bước tìm review liên quan nhất với câu hỏi.

Ví dụ:

```text
Query: Khách hàng phàn nàn gì về giao hàng chậm?
```

Hệ thống sẽ ưu tiên review có nội dung như:

- giao lâu,
- ship trễ,
- vận chuyển chậm,
- shop xử lý đơn lâu.

## RAG là gì trong project này?

RAG ở đây là dạng **evidence-grounded answer generation**:

```text
Query -> retrieve review liên quan -> tạo câu trả lời dựa trên evidence
```

Answer generator hiện là template-based, không gọi LLM bên ngoài. Điều này giúp demo chạy ổn định, không cần API key và không bịa ngoài dữ liệu.

## Output

```text
results/module4/rag_outputs.json
results/module4/rag_outputs.md
results/module4/rag_outputs_upgraded.json
results/module4/rag_outputs_upgraded_smoke.json
results/module4/retrieval_eval_summary.csv
results/module4/manual_precision_at_k_sheet.csv
results/module4/last_retrieval_results.csv
```

## Đánh giá retrieval

Theo `results/module5/manual_precision_overall.csv`:

- Precision@3: khoảng **0.422**
- Precision@5: khoảng **0.507**
- Precision@10: khoảng **0.487**

Đây là baseline/manual evaluation hiện có, không phải điểm tự động của giao diện mới.

## Liên kết với sentiment

RAG dùng sentiment như metadata filter:

- câu hỏi có `phàn nàn`, `lỗi`, `hỏng`, `chậm` -> ưu tiên review `negative`;
- câu hỏi hỏi điểm tốt -> có thể ưu tiên review `positive`;
- người dùng vẫn có thể tắt filter tự động trong giao diện.

## Cách chạy lại Module 4 gốc

```bash
bash scripts/run_module4.sh
```

## Khi nào cần build lại index?

Cần build lại nếu thay corpus, embedding model hoặc cách tạo text retrieval.

Không cần build lại nếu chỉ sửa frontend, backend display, README hoặc format answer.

## Liên hệ với Module 6

Module 4 là retrieval/RAG chính dùng trong web demo. Module 6 là hướng nâng cấp kỹ thuật dùng lại artifact Module 4:

```text
models/module4/review_faiss.index
models/module4/review_metadata.parquet
data/processed/rag_corpus_module4.csv
```

Module 6 bổ sung BM25, RRF fusion, optional reranker và rule-based aspect sentiment. Nó không thay thế Module 4 trong web demo hiện tại, mà dùng để chứng minh hướng cải thiện retrieval.
