# Giải thích dự án Vietnamese E-commerce Sentiment + RAG cho người mới

## 1. Dự án này giải quyết bài toán gì?

Tên đề tài:

```text
Ứng dụng Xử lý ngôn ngữ tự nhiên và Retrieval-Augmented Generation trong phân tích cảm xúc đánh giá sản phẩm TMĐT
```

Dự án xử lý review sản phẩm thương mại điện tử tiếng Việt. Có 2 mục tiêu:

- Phân tích cảm xúc review: review là tiêu cực, trung lập hay tích cực.
- Hỏi đáp bằng RAG: người dùng hỏi một vấn đề, hệ thống tìm review liên quan và trả lời kèm bằng chứng.

Ví dụ:

```text
Review: "Shop giao sai màu, nhắn tin không trả lời."
Sentiment: Tiêu cực

Câu hỏi RAG: "Khách hàng phàn nàn gì về giao hàng chậm?"
Output: Tóm tắt các vấn đề và trích dẫn review liên quan.
```

Nói đơn giản: **model sentiment giúp biết cảm xúc của từng review; RAG giúp gom bằng chứng từ nhiều review để trả lời câu hỏi.**

## 2. Kiến thức nền cần biết

### NLP là gì?

NLP là xử lý ngôn ngữ tự nhiên. Trong project này, NLP dùng để xử lý review tiếng Việt.

### Sentiment Classification là gì?

Là bài toán phân loại cảm xúc của văn bản. Input là review, output là nhãn:

- `negative`: Tiêu cực
- `neutral`: Trung lập
- `positive`: Tích cực

### RAG là gì?

RAG là Retrieval-Augmented Generation. Ý tưởng:

```text
Tìm tài liệu liên quan trước -> tạo câu trả lời dựa trên tài liệu đó
```

Trong project này, tài liệu là review sản phẩm. Câu trả lời không bịa ngoài dữ liệu, mà phải dựa vào review được truy xuất.

### FAISS là gì?

FAISS là thư viện tìm kiếm vector nhanh. Nó giúp tìm review có embedding gần với embedding của câu hỏi.

### Embedding là gì?

Embedding là vector số biểu diễn ý nghĩa của text. Hai câu gần nghĩa sẽ có vector gần nhau.

Ví dụ:

```text
"giao hàng chậm"
"ship lâu"
```

Hai câu khác chữ nhưng gần nghĩa, nên embedding có thể giúp tìm ra chúng.

## 3. Cấu trúc thư mục

```text
data/                 Dữ liệu đã xử lý và query đánh giá
src/                  Code chính của các module
scripts/              Script chạy module, chạy app, đóng gói
models/               Model sentiment và FAISS index
results/              Metric, prediction, RAG output
figures/              Biểu đồ
report/               Nội dung báo cáo
frontend/             Giao diện web demo
backend/              API FastAPI cho demo
README_MODULE*.md     Giải thích từng module
README_DEMO.md        Hướng dẫn chạy/quay demo
README_RAG_WEBAPP.md  Giải thích web app
artifact_manifest.json Danh sách file trong gói nộp kèm hash
```

## 4. Luồng xử lý end-to-end

```text
Raw data
  |
  v
Module 1: Data Layer
  - làm sạch review
  - tạo sentiment_reviews.csv
  - tạo rag_corpus_module4.csv
  |
  v
Module 2: Sentiment Classification
  - train TF-IDF + Logistic Regression
  - train TF-IDF + Linear SVM
  - chọn best_model.joblib
  |
  v
Module 3: Review Analytics
  - thống kê sentiment/rating
  - tạo bảng và biểu đồ
  |
  v
Module 4: Retrieval/RAG
  - dùng multilingual-E5 tạo embedding
  - build FAISS index
  - retrieve review liên quan
  - tạo answer có evidence
  |
  v
Module 6: Hybrid Retrieval nâng cấp
  - BM25 keyword search
  - Dense FAISS retrieval
  - RRF fusion/rerank
  - aspect-aware evidence
  |
  v
Module 5: Evaluation & Report
  - tổng hợp metric
  - phân tích lỗi
  - tạo nội dung báo cáo
  |
  v
Web demo
  - Tab Sentiment
  - Tab RAG
  - Tab Kỹ thuật & đánh giá
```

## 5. Module 1: Data Layer

File chính:

```text
src/module1_data_layer.py
```

Module này đọc dữ liệu, làm sạch và tạo các file processed.

Các việc quan trọng:

- chuẩn hóa text review,
- chuẩn hóa rating,
- tạo nhãn sentiment,
- xử lý duplicate,
- chia train/valid/test,
- tạo corpus cho RAG.

Cột quan trọng:

- `text`: nội dung review dùng cho sentiment model.
- `rating`: số sao.
- `sentiment`: nhãn cảm xúc.
- `retrieval_text`: text dùng để tìm kiếm trong RAG.

Vì sao cần duplicate handling? Nếu một review xuất hiện nhiều lần, model có thể học thuộc hoặc kết quả đánh giá bị lệch.

Output chính:

```text
data/processed/sentiment_reviews.csv
data/processed/sentiment_reviews_5class.csv
data/processed/rag_corpus_module4.csv
```

## 6. Module 2: Sentiment Classification

File chính:

```text
src/module2_baseline_sentiment_classification.py
```

Module này huấn luyện model sentiment.

Model được thử:

- Majority baseline.
- TF-IDF + Logistic Regression.
- TF-IDF + Linear SVM.

TF-IDF là cách biến câu thành vector. Từ càng đặc trưng thì trọng số càng cao.

Ví dụ nếu review có nhiều từ như `lỗi`, `tệ`, `không trả lời`, model có thể học rằng review này dễ là `negative`.

Kết quả bản final:

- Majority baseline test macro-F1: khoảng `0.200`.
- Logistic Regression test macro-F1: khoảng `0.894`.
- Linear SVM test macro-F1: khoảng `0.910`.

Model chính:

```text
models/module2/best_model.joblib
```

Nói đơn giản: **đây là model sentiment thật sự của project.**

## 7. Module 3: Review Analytics

Module 3 không train model. Nó tạo thống kê và biểu đồ.

Output:

```text
results/module3/overall_sentiment_distribution.csv
results/module3/rating_sentiment_crosstab.csv
results/module3/top_negative_reviews.csv
figures/module3/
```

Dùng để trả lời:

- review tiêu cực nhiều hay ít,
- rating và sentiment có khớp không,
- các review tiêu cực tiêu biểu là gì.

Nói đơn giản: **Module 3 giúp biến dữ liệu sentiment thành insight cho báo cáo.**

## 8. Module 4: Retrieval/RAG

File gốc:

```text
src/module4_prepare_inputs.py
src/module4_build_index.py
src/module4_retrieve.py
src/module4_rag_pipeline.py
src/module4_evaluate.py
```

File nâng cấp dùng trong demo:

```text
src/module4_retrieve_upgraded.py
src/module4_rag_pipeline_upgraded.py
```

Artifact:

```text
models/module4/review_faiss.index
models/module4/review_metadata.parquet
models/module4/module4_index_config.json
```

Thông tin bản final:

- Corpus: `82.677 review/documents`.
- Embedding model: `intfloat/multilingual-e5-small`.
- FAISS index: `IndexFlatIP`.
- Retrieval method: Dense FAISS + query expansion + lightweight rerank.

Luồng RAG:

```text
User query
  -> nhận diện aspect/filter
  -> mở rộng query
  -> encode query bằng multilingual-E5
  -> FAISS tìm review gần nhất
  -> rerank nhẹ bằng keyword/aspect
  -> tạo câu trả lời có citation
```

Ví dụ query expansion:

```text
giao hàng chậm -> ship trễ, giao lâu, vận chuyển lâu, nhận hàng chậm
```

Nói đơn giản: **RAG không tự tưởng tượng; nó tìm review thật rồi trả lời dựa trên review đó.**

## 9. Module 5: Evaluation & Report

File chính:

```text
src/module5_collect_results.py
src/module5_manual_retrieval_eval.py
src/module5_error_analysis.py
src/module5_generate_figures.py
src/module5_generate_report_sections.py
```

Output:

```text
results/module5/final_metrics_summary.csv
results/module5/final_project_summary.json
results/module5/manual_precision_overall.csv
results/module5/error_analysis.md
report/final_report_sections.md
```

Precision@5 hiện có:

```text
0.50667
```

Nghĩa là trung bình trong 5 review truy xuất đầu tiên, khoảng 50.7% được chấm là liên quan theo đánh giá thủ công.

## 9.5. Module 6: Aspect-aware Hybrid Retrieval

Module 6 là phần nâng cấp kỹ thuật cho retrieval. Nó không thay thế app demo chính, nhưng bổ sung hướng tìm evidence tốt hơn.

File chính:

```text
src/module6_hybrid_retrieval.py
src/module6_reranker.py
src/module6_aspect_sentiment.py
src/module6_query_intent.py
scripts/run_module6_hybrid_rerank_demo.py
scripts/evaluate_module6_retrieval.py
```

Ý tưởng:

```text
BM25 tìm review trùng từ khóa complaint
Dense FAISS tìm review gần nghĩa
RRF fusion gộp hai ranking
Reranker/aspect rules ưu tiên evidence đúng chủ đề
```

Ví dụ:

```text
Query: "Khách phàn nàn gì về đóng gói?"
BM25 bắt các từ như "móp hộp", "rách", "sơ sài"
Dense FAISS bắt các review gần nghĩa dù không trùng y hệt từ khóa
```

Chạy thử:

```powershell
python scripts\run_module6_hybrid_rerank_demo.py --query "Khách phàn nàn gì về giao hàng?" --top-candidates 50 --top-evidence 5 --use-reranker false --target-aspect giao_hang
```

Nói đơn giản: **Module 6 là bản nâng cấp retrieval để tìm evidence theo aspect tốt hơn, nhưng vẫn không phải LLM sinh tự do.**

## 10. Các file model quan trọng

```text
models/module2/best_model.joblib
```

Model sentiment chính dùng ở tab `Phân tích Sentiment`.

```text
models/module2/tfidf_linearsvm.joblib
models/module2/tfidf_logreg.joblib
```

Các model sentiment đã train.

```text
models/module2/label_mapping.json
```

Mapping nhãn sentiment.

```text
models/module4/review_faiss.index
```

Vector index để tìm review liên quan.

```text
models/module4/review_metadata.parquet
```

Metadata tương ứng với từng vector trong FAISS.

```text
models/module4/module4_index_config.json
```

Cấu hình index: model embedding, số documents, đường dẫn artifact.

## 11. Cách chạy project

Cài thư viện:

```powershell
python -m pip install -r requirements_webapp.txt
python -m pip install -r requirements_module4.txt
```

Chạy app:

```powershell
python scripts\run_rag_webapp.py
```

Mở:

```text
http://127.0.0.1:8000
```

Đóng gói:

```powershell
python scripts\package_final_submission.py
```

## 12. Cách đọc kết quả

### Sentiment output

Xem:

```text
results/module2/metrics_summary.csv
```

Các metric chính:

- accuracy,
- precision,
- recall,
- macro-F1.

Model tốt nhất là Linear SVM vì test macro-F1 cao nhất trong các baseline.

### RAG output

Xem:

```text
results/module4/rag_outputs_upgraded_smoke.json
results/module4/rag_outputs.md
```

Trong web demo, xem trực tiếp:

- `Tóm tắt`,
- `Các vấn đề chính`,
- `Bằng chứng tiêu biểu`,
- `Độ tin cậy`,
- `Review được truy xuất`.

### Evaluation output

Xem:

```text
results/module5/final_metrics_summary.csv
results/module5/manual_precision_overall.csv
```

## 13. Các thuật ngữ quan trọng

| Thuật ngữ | Định nghĩa đơn giản | Xuất hiện ở đâu | Ví dụ |
|---|---|---|---|
| NLP | Xử lý ngôn ngữ tự nhiên | Toàn project | xử lý review tiếng Việt |
| Sentiment Analysis | Phân tích cảm xúc | Module 2, tab Sentiment | review tiêu cực |
| Classification | Phân loại | Module 2 | negative/neutral/positive |
| Label | Nhãn đúng/dự đoán | dữ liệu sentiment | `negative` |
| Train/Validation/Test | Chia dữ liệu học/chọn/kiểm tra | Module 1, 2 | train model rồi test |
| TF-IDF | Vector hóa text theo trọng số từ | Module 2 | từ `lỗi` có trọng số cao |
| Logistic Regression | Model tuyến tính phân loại | Module 2 | baseline mạnh |
| Linear SVM | Model tuyến tính mạnh cho text | Module 2 | best model |
| Baseline | Mốc so sánh | Module 2 | majority baseline |
| Accuracy | Tỷ lệ đúng | metrics_summary | 0.933 |
| Precision | Độ chính xác khi dự đoán một lớp | classification report | dự đoán negative có đúng không |
| Recall | Tìm được bao nhiêu mẫu thật | classification report | bắt được bao nhiêu review negative |
| F1-score | Cân bằng precision/recall | Module 2 | F1 negative |
| Macro-F1 | F1 trung bình đều các lớp | chọn model | dùng vì class lệch |
| Embedding | Vector biểu diễn nghĩa | Module 4 | vector câu hỏi |
| multilingual-E5 | Model embedding đa ngôn ngữ | Module 4 | `intfloat/multilingual-e5-small` |
| FAISS | Thư viện tìm vector gần nhất | Module 4 | review_faiss.index |
| Retrieval | Truy xuất tài liệu liên quan | Module 4 | tìm top-5 review |
| Top-k | Số kết quả lấy ra | RAG UI | top_k = 5 |
| RAG | Retrieval + Answer generation | Module 4 | trả lời có bằng chứng |
| Metadata filtering | Lọc theo thông tin phụ | Module 4 | sentiment negative |
| Evidence | Bằng chứng | RAG output | review được cite |
| Citation | Trích dẫn | RAG output | `[1]`, `[2]` |
| Error analysis | Phân tích lỗi | Module 5 | model sai lớp neutral |

## 14. Hạn chế của project

- Sentiment label có thể nhiễu vì mapping từ rating sang sentiment không phải lúc nào cũng đúng.
- TF-IDF + SVM không hiểu ngữ cảnh sâu như PhoBERT/BERT.
- RAG retrieval có thể lấy review không liên quan nếu query quá chung.
- Precision@5 của retrieval còn ở mức baseline khoảng 0.507.
- Answer generator là template-based, không phải LLM thật.
- Nếu evidence yếu, hệ thống chỉ nên nói chưa đủ bằng chứng thay vì kết luận mạnh.

## 15. Nếu muốn cải tiến thì làm gì?

Ưu tiên cải tiến theo thứ tự:

1. Fine-tune PhoBERT/XLM-R cho sentiment để so sánh với TF-IDF + SVM.
2. Tạo bộ đánh giá retrieval lớn hơn và chấm nhất quán hơn.
3. Dùng Module 6 để thử hybrid retrieval BM25 + dense embedding.
4. Dùng Module 6 để thử RRF fusion và cross-encoder reranker nếu máy đủ mạnh.
5. Dùng LLM thật để viết answer, nhưng bắt buộc bám vào evidence.
6. Cải thiện dữ liệu RAG, loại review nhiễu và duplicate.

## 16. Tóm tắt cực ngắn cho người không chuyên

Project này đọc review sản phẩm TMĐT tiếng Việt. Model sentiment cho biết review là tiêu cực, trung lập hay tích cực. RAG cho phép người dùng hỏi như "khách hàng phàn nàn gì về giao hàng?" và hệ thống sẽ tìm các review liên quan để trả lời kèm bằng chứng. Web demo có 3 tab: phân tích sentiment, hỏi đáp RAG, và thông tin kỹ thuật/đánh giá.

## Checklist học project

- Đọc `README_DEMO.md` trước để biết cách chạy và quay demo.
- Đọc `README_MODULE2.md` để hiểu model sentiment.
- Đọc `README_MODULE4.md` để hiểu RAG.
- Mở web app và test Tab Sentiment trước.
- Sau đó test Tab RAG với câu hỏi về giao hàng, chất lượng, sai hàng.
- Cuối cùng mở Tab Kỹ thuật để xem model/index/metric.
