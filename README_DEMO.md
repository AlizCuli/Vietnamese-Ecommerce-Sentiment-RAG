# README DEMO - Vietnamese E-commerce Sentiment + RAG

## 1. Tên đề tài

**Ứng dụng Xử lý ngôn ngữ tự nhiên và Retrieval-Augmented Generation trong phân tích cảm xúc đánh giá sản phẩm TMĐT**

Project này có 2 phần chính và 1 phần nâng cấp kỹ thuật:

- **Sentiment Classification**: phân loại cảm xúc review sản phẩm thành `Tiêu cực`, `Trung lập`, `Tích cực`.
- **RAG có bằng chứng**: truy xuất review liên quan bằng FAISS + embedding, sau đó tạo câu trả lời có citation `[1]`, `[2]`, `[3]`.
- **Module 6 Hybrid Retrieval**: hướng nâng cấp retrieval bằng BM25 + Dense FAISS + aspect-aware reranking.

Trong demo, nên trình bày **Sentiment trước**, vì đây là bài toán NLP chính. Sau đó trình bày RAG như phần mở rộng giúp hỏi đáp và giải thích bằng review thật.

## 2. Cấu trúc quan trọng

```text
backend/                  API FastAPI cho web demo
frontend/                 Giao diện web 3 tab
src/                      Code các module xử lý NLP/RAG
scripts/                  Script chạy module, chạy app, đóng gói
data/processed/           Dữ liệu đã chuẩn hóa
models/module2/           Artifact model sentiment
models/module4/           Artifact FAISS index và metadata RAG
results/                  Kết quả đánh giá, prediction, output mẫu
figures/                  Biểu đồ dùng cho báo cáo
report/                   Nội dung báo cáo markdown
README_MODULE*.md         Giải thích từng module
README_RAG_WEBAPP.md      Giải thích web app
EXPLAIN_PROJECT_FOR_BEGINNER.md  Tài liệu học project cho người mới
```

Trong đó `README_MODULE6.md` giải thích phần hybrid retrieval nâng cấp.

## 3. Cách chạy app demo

Mở PowerShell tại thư mục project:

```powershell
cd "C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted"
```

Cài thư viện nếu máy chưa có:

```powershell
python -m pip install -r requirements_webapp.txt
python -m pip install -r requirements_module4.txt
```

Chạy web app:

```powershell
python scripts\run_rag_webapp.py
```

Mở trình duyệt:

```text
http://127.0.0.1:8000
```

Nếu app đang mở mà giao diện chưa đổi, bấm `Ctrl + F5`.

## 4. Luồng demo 5 phút gợi ý

### Phần 1: Giới thiệu đề tài

Nói ngắn:

```text
Đề tài dùng NLP để phân tích cảm xúc review TMĐT. Sau đó dùng RAG để tìm các review liên quan và tạo câu trả lời có bằng chứng, giúp người dùng hiểu khách hàng đang phàn nàn/khen về vấn đề gì.
```

### Phần 2: Tab Phân tích Sentiment

1. Mở tab `Phân tích Sentiment`.
2. Nhập một review thật, ví dụ:

```text
Shop giao sai màu, nhắn tin hỗ trợ nhưng không trả lời.
```

3. Bấm `Phân tích sentiment`.
4. Giải thích output:

- `Cảm xúc`: dự đoán Tiêu cực / Trung lập / Tích cực.
- `Model`: model đang dùng là artifact ở `models/module2/best_model.joblib`.
- `Confidence/margin`: độ tự tin tương đối của model nếu có.

### Phần 3: Tab Hỏi đáp RAG

1. Mở tab `Hỏi đáp RAG`.
2. Nhập câu hỏi:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
```

3. Bấm `Chạy RAG`.
4. Giải thích các phần:

- `Hệ thống hiểu câu hỏi`: nhận diện aspect, sentiment filter, query mở rộng.
- `Câu trả lời có bằng chứng`: tóm tắt, vấn đề chính, evidence, độ tin cậy.
- `Review được truy xuất`: các review thật tương ứng với citation `[1]`, `[2]`, `[3]`.
- `Chi tiết kỹ thuật`: thông tin FAISS, embedding model, filters, thời gian truy xuất.

### Phần 4: Tab Kỹ thuật & đánh giá

Nói các thông tin chính:

- Kho RAG hiện có **82.677 review/documents**.
- Embedding model: `intfloat/multilingual-e5-small`.
- Retrieval: Dense FAISS + query expansion + lightweight rerank.
- Baseline/manual Precision@5 hiện có: khoảng **0.507**.
- Sentiment model tốt nhất: TF-IDF + Linear SVM, test macro-F1 khoảng **0.910**.
- Module 6 là hướng nâng cấp thêm: BM25 + Dense FAISS + RRF/rerank theo aspect.

## 5. Model và RAG liên kết với nhau như thế nào?

Hai phần không bị trộn lẫn input:

- Sentiment tab nhận **review sản phẩm thật** để phân loại cảm xúc.
- RAG tab nhận **câu hỏi của người dùng** để truy xuất review.

Chúng liên kết ở tầng dữ liệu và phân tích:

- Corpus RAG có trường `predicted_sentiment` để ưu tiên lọc review tiêu cực/tích cực.
- Khi câu hỏi có từ như `phàn nàn`, `lỗi`, `giao chậm`, hệ thống tự ưu tiên sentiment `Tiêu cực`.
- RAG dùng sentiment như metadata filter, không phân tích câu hỏi RAG như một review.

## 6. File model và artifact quan trọng

```text
models/module2/best_model.joblib
```

Model sentiment chính dùng cho Tab `Phân tích Sentiment`.

```text
models/module4/review_faiss.index
models/module4/review_metadata.parquet
models/module4/module4_index_config.json
```

Artifact RAG dùng cho Tab `Hỏi đáp RAG`.

```text
data/processed/rag_corpus_module4.csv
```

Corpus RAG đã mở rộng và chuẩn hóa.

## 7. Đóng gói file nộp bài

Chạy:

```powershell
python scripts\package_final_submission.py
```

Script sẽ tạo:

```text
ecommerce_sentiment_rag_final_submission.zip
artifact_manifest.json
```

File zip đã bao gồm code, frontend, backend, dữ liệu processed, model artifacts, results, figures, report và README.

## 8. Checklist trước khi nộp

- Chạy được `python scripts\run_rag_webapp.py`.
- Mở được `http://127.0.0.1:8000`.
- Tab `Phân tích Sentiment` dự đoán được một review.
- Tab `Hỏi đáp RAG` trả lời được câu hỏi và có evidence cards.
- Tab `Kỹ thuật & đánh giá` hiển thị được kho review, model, Precision@5.
- File `ecommerce_sentiment_rag_final_submission.zip` đã được tạo lại sau khi sửa tài liệu.

## 9. Lưu ý

- Không cần API key.
- Không dùng LLM thật; answer generator là template-based, bám vào evidence.
- Nếu chỉ sửa giao diện/tài liệu thì không cần rebuild FAISS.
- Nếu thay corpus hoặc embedding model thì phải build lại `review_faiss.index` và `review_metadata.parquet`.
- Module 6 dùng lại corpus/index hiện có; không tự rebuild FAISS.
