# README MODULE 5 - Final Evaluation and Report

## Vai trò

Module 5 tổng hợp kết quả từ các module trước để phục vụ báo cáo cuối kỳ.

Nói đơn giản: **Module 5 gom metric, phân tích lỗi, kết quả RAG và nội dung báo cáo vào một nơi.**

## Input chính

```text
results/module2/metrics_summary.csv
results/module2/linear_svm_classification_report.csv
results/module2/logistic_regression_classification_report.csv
results/module4/rag_outputs.json
results/module4/retrieval_eval_summary.csv
results/module4/manual_precision_at_k_sheet.csv
```

Input bổ sung nếu có:

```text
results/module3/overall_sentiment_distribution.csv
results/module3/rating_sentiment_crosstab.csv
results/module3/rag_sentiment_summary.json
```

## File code chính

```text
src/module5_collect_results.py
src/module5_manual_retrieval_eval.py
src/module5_error_analysis.py
src/module5_generate_figures.py
src/module5_generate_report_sections.py
```

## Các bước Module 5

1. `module5_collect_results.py`: gom metric từ Module 2, 3, 4.
2. `module5_manual_retrieval_eval.py`: tính Precision@k nếu đã có chấm liên quan.
3. `module5_error_analysis.py`: tạo phân tích lỗi cho sentiment và RAG.
4. `module5_generate_figures.py`: tạo biểu đồ tổng hợp.
5. `module5_generate_report_sections.py`: tạo nội dung markdown cho báo cáo.

## Output

```text
results/module5/final_metrics_summary.csv
results/module5/final_project_summary.json
results/module5/manual_precision_summary.csv
results/module5/manual_precision_overall.csv
results/module5/error_analysis.md
results/module5/final_discussion.md
results/module5/final_conclusion.md
figures/module5/
report/report_skeleton.md
report/final_report_sections.md
```

## Manual Precision@k là gì?

Precision@k đo trong top-k review hệ thống trả về, có bao nhiêu review thật sự liên quan.

Ví dụ Precision@5 = 0.507 nghĩa là trung bình trong 5 review đầu, khoảng 50.7% được chấm là liên quan theo sheet thủ công.

## Có cần chạy lại Module 5 không?

Cần chạy lại nếu:

- thay kết quả Module 2,
- thay kết quả đánh giá RAG,
- thay manual judgement sheet,
- muốn tạo lại báo cáo/metric.

Không bắt buộc chạy lại nếu chỉ sửa giao diện hoặc README.

## Cách chạy

Trên Linux/macOS/Colab:

```bash
bash scripts/run_module5.sh
```

Trên Windows PowerShell:

```powershell
python src\module5_collect_results.py
python src\module5_manual_retrieval_eval.py
python src\module5_error_analysis.py
python src\module5_generate_figures.py
python src\module5_generate_report_sections.py
```

## Đóng gói nộp bài

Sau khi mọi thứ đã ổn, chạy:

```powershell
python scripts\package_final_submission.py
```

Script sẽ tạo file zip nộp bài và cập nhật `artifact_manifest.json`.
