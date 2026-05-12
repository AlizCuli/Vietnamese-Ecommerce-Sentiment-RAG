# README MODULE 1 - Data Layer

## Vai trò

Module 1 là tầng chuẩn hóa dữ liệu. Module này biến dữ liệu thô thành các file sạch để Module 2 huấn luyện sentiment model và Module 4 xây dựng RAG corpus.

Nói đơn giản: **Module 1 là bước dọn dữ liệu trước khi học máy và truy xuất.**

## Input

Nguồn dữ liệu ban đầu gồm:

- dữ liệu sentiment review cho phần model,
- dữ liệu review JSON cho phần RAG.

Trong project đã đóng gói, dữ liệu đã xử lý nằm ở:

```text
data/processed/sentiment_reviews.csv
data/processed/sentiment_reviews_5class.csv
data/processed/rag_documents.jsonl
data/processed/rag_corpus.csv
data/processed/rag_corpus_module4.csv
```

## File code chính

```text
src/module1_data_layer.py
```

File này làm sạch dữ liệu, chuẩn hóa cột, xử lý duplicate, tạo split và xuất báo cáo dữ liệu.

## Các việc Module 1 thực hiện

- Chuẩn hóa cột review text.
- Chuẩn hóa rating.
- Tạo nhãn sentiment:
  - `1-2 sao` -> `negative`
  - `3 sao` -> `neutral`
  - `4-5 sao` -> `positive`
- Xử lý duplicate để tránh review lặp gây lệch dữ liệu.
- Chia `train/valid/test` cho sentiment model.
- Tạo corpus review cho RAG.
- Xuất báo cáo phân phối nhãn/category.

## Vì sao cần train/valid/test?

- `train`: dùng để huấn luyện model.
- `valid`: dùng để chọn cấu hình tốt nhất.
- `test`: chỉ dùng một lần cuối để đánh giá khách quan.

Nếu dùng test để chọn model, kết quả sẽ bị lạc quan giả.

## Output

```text
data/processed/sentiment_reviews.csv
data/processed/sentiment_reviews_5class.csv
data/processed/sentiment_duplicates_report.csv
data/processed/rag_documents.jsonl
data/processed/rag_corpus.csv
data/reports/data_summary.json
data/reports/sentiment_label_distribution.csv
data/reports/rag_category_split_distribution.csv
figures/module1/
```

## Cách chạy lại

```bash
bash scripts/run_module1.sh
```

Trên Windows PowerShell, có thể chạy trực tiếp:

```powershell
python src\module1_data_layer.py
```

## Lưu ý bản final

Trong bản demo cuối, RAG dùng corpus đã nâng cấp:

```text
data/processed/rag_corpus_module4.csv
```

File này có **82.677 review/documents** và được dùng để build FAISS index ở Module 4.
