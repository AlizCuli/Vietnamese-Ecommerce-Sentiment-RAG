# README RAG WEBAPP

## 1. Mục tiêu web app

Web app là bản demo trực quan cho đề tài:

```text
Ứng dụng NLP và RAG trong phân tích cảm xúc đánh giá sản phẩm TMĐT
```

App có 3 tab:

1. `Phân tích Sentiment`: chạy model sentiment trên một review thật.
2. `Hỏi đáp RAG`: đặt câu hỏi về review và nhận câu trả lời có bằng chứng.
3. `Kỹ thuật & đánh giá`: xem thông tin corpus, model, index, metric và export kết quả.

## 2. File giao diện và backend

```text
frontend/index.html    Bố cục HTML của app
frontend/styles.css    Thiết kế responsive, card, tab, badge, evidence
frontend/app.js        State management, gọi API, render output
backend/app.py         FastAPI backend cho sentiment và RAG
scripts/run_rag_webapp.py  Lệnh chạy server local
```

## 3. Backend API

### `GET /api/health`

Kiểm tra backend đã load được resource chưa.

### `GET /api/config`

Trả về thông tin cấu hình:

- số documents trong kho RAG,
- embedding model,
- retrieval method,
- baseline Precision@5,
- category thật trong metadata,
- đường dẫn artifact dạng tương đối.

### `POST /api/sentiment`

Input:

```json
{
  "text": "Shop giao sai màu, nhắn tin không trả lời."
}
```

Output:

```json
{
  "label": "negative",
  "label_vi": "Tiêu cực",
  "model_path": "models/module2/best_model.joblib"
}
```

Endpoint này chỉ dùng cho review sản phẩm thật, không dùng cho câu hỏi RAG.

### `POST /api/rag`

Input chính:

```json
{
  "query": "Khách hàng phàn nàn gì về giao hàng chậm?",
  "top_k": 5,
  "sentiment": "auto",
  "category": "all",
  "rating_filter": "all",
  "auto_filter": true,
  "smart_category": true,
  "exclude_app": true,
  "evidence_only": true
}
```

Output chính:

- `answer`: câu trả lời đã format.
- `summary`: tóm tắt ngắn.
- `main_issues`: các vấn đề chính.
- `evidence`: review liên quan có citation.
- `confidence`: độ tin cậy.
- `understanding`: hệ thống hiểu query như thế nào.
- `diagnostics`: thông tin kỹ thuật.

## 4. State management trong frontend

Frontend lưu:

- `lastRunQuery`: câu hỏi đã chạy thật sự.
- `currentRagResult`: kết quả RAG gần nhất.
- `currentConfig`: thông tin config từ backend.

Nếu người dùng sửa câu hỏi sau khi đã có output nhưng chưa bấm `Chạy RAG`, app hiển thị cảnh báo:

```text
Câu hỏi đã thay đổi. Hãy bấm Chạy RAG để cập nhật kết quả.
```

Điều này tránh hiểu nhầm output cũ là kết quả của câu hỏi mới.

## 5. Logic RAG trong app

Luồng xử lý:

```text
Query người dùng
  -> infer_filters_from_query()
  -> expand_vietnamese_query()
  -> ReviewRetriever.retrieve()
  -> build_evidence_items()
  -> generate_answer()
  -> frontend render thành answer cards + evidence cards
```

Nếu câu hỏi có dấu hiệu phàn nàn như `chậm`, `lỗi`, `hỏng`, `sai hàng`, hệ thống ưu tiên sentiment `negative`.

Nếu câu hỏi nói về `size`, hệ thống có thể ưu tiên category `Fashion`.

Nếu evidence yếu, output phải nói:

```text
Chưa đủ bằng chứng rõ ràng từ các review được truy xuất.
```

## 6. Có cần rebuild FAISS không?

Không cần rebuild nếu chỉ sửa:

- giao diện,
- CSS,
- JavaScript,
- format output,
- README.

Cần rebuild nếu thay:

- file corpus `data/processed/rag_corpus_module4.csv`,
- embedding model,
- cách tạo `retrieval_text`,
- metadata dùng cho filtering.

## 7. Cách chạy

```powershell
python -m pip install -r requirements_webapp.txt
python scripts\run_rag_webapp.py
```

Mở:

```text
http://127.0.0.1:8000
```

## 8. Test nhanh

- Tab Sentiment: nhập `Shop giao sai màu, nhắn tin không trả lời.`
- Tab RAG: hỏi `Khách hàng phàn nàn gì về giao hàng chậm?`
- Tab RAG: hỏi `Có review nào nói hàng bị lỗi hoặc hỏng không?`
- Tab kỹ thuật: kiểm tra số documents là `82.677`.
- Đổi query sau khi có output: phải hiện cảnh báo cần chạy lại.
