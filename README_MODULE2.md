# README MODULE 2 - Sentiment Classification

## Vai trò

Module 2 là phần model NLP chính của đề tài. Module này huấn luyện model phân loại cảm xúc review TMĐT tiếng Việt.

Nói đơn giản: **người dùng đưa một review vào, model dự đoán review đó Tiêu cực / Trung lập / Tích cực.**

## Input

```text
data/processed/sentiment_reviews.csv
```

Các cột quan trọng:

- `text`: nội dung review.
- `rating`: số sao.
- `sentiment`: nhãn 3 lớp.
- `split`: train/valid/test.

## File code chính

```text
src/module2_baseline_sentiment_classification.py
```

File này huấn luyện các baseline model và chọn model tốt nhất theo validation macro-F1.

## Model được thử

### Majority baseline

Luôn dự đoán lớp xuất hiện nhiều nhất. Đây là mốc so sánh tối thiểu.

### TF-IDF + Logistic Regression

TF-IDF biến text thành vector dựa trên độ quan trọng của từ. Logistic Regression học ranh giới giữa các lớp sentiment.

### TF-IDF + Linear SVM

Linear SVM rất mạnh cho text classification vì dữ liệu TF-IDF thường có nhiều chiều và thưa.

## Metric chính

- `Accuracy`: tỷ lệ dự đoán đúng toàn bộ.
- `Precision`: dự đoán một lớp có chính xác không.
- `Recall`: model tìm được bao nhiêu mẫu thật của lớp đó.
- `F1-score`: cân bằng giữa precision và recall.
- `Macro-F1`: F1 trung bình đều trên các lớp, phù hợp khi class lệch.

## Kết quả bản final

Theo `results/module2/metrics_summary.csv`:

- Majority baseline test macro-F1: khoảng **0.200**.
- Logistic Regression test macro-F1: khoảng **0.894**.
- Linear SVM test macro-F1: khoảng **0.910**.

Model tốt nhất là **TF-IDF + Linear SVM**, được lưu tại:

```text
models/module2/best_model.joblib
```

## Output

```text
models/module2/best_model.joblib
models/module2/tfidf_logreg.joblib
models/module2/tfidf_linearsvm.joblib
models/module2/label_mapping.json
results/module2/metrics_summary.csv
results/module2/metrics_summary.json
results/module2/tuning_results.csv
results/module2/*classification_report.csv
results/module2/*predictions.csv
results/module2/error_analysis_*.csv
figures/module2/
```

## Liên kết với web demo

Tab `Phân tích Sentiment` trong web app load:

```text
models/module2/best_model.joblib
```

để dự đoán sentiment cho một review thật.

## Liên kết với RAG

Sentiment model và RAG không dùng chung input trực tiếp:

- Sentiment nhận review.
- RAG nhận câu hỏi.

Tuy nhiên, trong corpus RAG có trường sentiment để lọc review tiêu cực/tích cực. Vì vậy sentiment hỗ trợ RAG ở tầng metadata filter.

## Cách chạy lại

```bash
bash scripts/run_module2.sh
```

Trên Windows PowerShell:

```powershell
python src\module2_baseline_sentiment_classification.py
```
