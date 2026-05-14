# Bản đồ câu hỏi khi người khác chụp slide/source code hỏi chatbot

Tài liệu này dùng để chuẩn bị bảo vệ/thuyết trình. Mục tiêu là dự đoán những câu hỏi người khác có thể hỏi khi họ chụp slide, giao diện, bảng metric, JSON config hoặc source code rồi gửi lên chatbot.

Project final:

```text
C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted
```

PDF thuyết trình đã đọc:

```text
C:\Users\PC\Downloads\NLP.pdf
```

Nguyên tắc trả lời:

- Trả lời thẳng vào câu hỏi trước.
- Sau đó nói phương pháp/code/file chứng minh.
- Không nói quá mức. RAG của project là template-based/evidence-grounded, không phải LLM tự do.
- Nếu bị hỏi số liệu, dùng số final: RAG final có **82.677 documents**.

---

## 1. Câu trả lời tổng quan phải thuộc

Nếu bị hỏi "Project này làm gì?", trả lời:

> Project xây dựng hệ thống NLP cho review thương mại điện tử tiếng Việt. Hệ thống có hai phần chính: phân loại cảm xúc review bằng TF-IDF + Linear SVM, và hỏi đáp RAG bằng cách truy xuất review liên quan từ FAISS index rồi tạo câu trả lời có bằng chứng/citation.

Nếu bị hỏi "Bằng cách nào?", trả lời:

> Dữ liệu review được làm sạch và chia train/valid/test. Phần sentiment dùng TF-IDF để biến text thành vector và Linear SVM để phân loại negative/neutral/positive. Phần RAG dùng multilingual-E5 để encode review và query thành embedding, lưu review embedding trong FAISS, retrieve top-k review liên quan, rồi tạo câu trả lời theo template dựa trên evidence.

Nếu bị hỏi "Phương pháp chính là gì?", trả lời:

> Sentiment classification dùng TF-IDF + Linear SVM. Retrieval/RAG dùng multilingual-E5 + FAISS IndexFlatIP, query expansion, metadata filtering và template-based evidence-grounded answer generation. Module 6 thử nghiệm nâng cấp bằng BM25 + Dense FAISS + RRF/rerank + aspect rules.

---

## 2. Bản đồ source code nên mở khi bị hỏi

| Người hỏi muốn xem gì | Mở file | Dòng nên chỉ |
|---|---|---|
| Xử lý dữ liệu, clean text | `src/module1_data_layer.py` | `225-248`, `343-377` |
| Mapping rating sang sentiment | `src/module1_data_layer.py` | `365-373` |
| Xử lý duplicate/conflict duplicate | `src/module1_data_layer.py` | `384-444` |
| Chia train/valid/test | `src/module1_data_layer.py` | `454-501` |
| Tạo corpus RAG | `src/module1_data_layer.py` | `557-754` |
| Ghi summary data | `src/module1_data_layer.py` | `763-823` |
| Metric sentiment | `src/module2_baseline_sentiment_classification.py` | `205-260` |
| Pipeline Logistic Regression | `src/module2_baseline_sentiment_classification.py` | `423-449` |
| Pipeline Linear SVM | `src/module2_baseline_sentiment_classification.py` | `451-472` |
| Tuning và chọn model theo macro-F1 | `src/module2_baseline_sentiment_classification.py` | `476-542`, `608-662` |
| Lưu model `.joblib` | `src/module2_baseline_sentiment_classification.py` | `826-828` |
| Build FAISS index | `src/module4_build_index.py` | `77-115` |
| Load FAISS + metadata | `src/module4_retrieve.py` | `50-89` |
| Encode query E5 | `src/module4_retrieve.py` | `96-103` |
| Retrieve top-k | `src/module4_retrieve.py` | `154-202` |
| Query expansion RAG nâng cấp | `src/module4_retrieve_upgraded.py` | `146-157` |
| Auto sentiment filter | `src/module4_retrieve_upgraded.py` | `157-165`, `402-404` |
| Metadata filter category/sentiment/rating | `src/module4_retrieve_upgraded.py` | `299-325`, `417-436` |
| Rerank score nhẹ | `src/module4_retrieve_upgraded.py` | `340-452` |
| Detect issue/aspect trong answer | `src/module4_rag_pipeline_upgraded.py` | `159-222` |
| Độ tin cậy answer | `src/module4_rag_pipeline_upgraded.py` | `222-250` |
| Generate RAG answer | `src/module4_rag_pipeline_upgraded.py` | `302-341` |
| Module 6 BM25 fallback | `src/module6_hybrid_retrieval.py` | `29-84` |
| Module 6 BM25 retriever | `src/module6_hybrid_retrieval.py` | `146-158` |
| Module 6 Dense retriever wrapper | `src/module6_hybrid_retrieval.py` | `258-285` |
| Module 6 RRF fusion | `src/module6_hybrid_retrieval.py` | `289-386` |
| Module 6 query intent/aspect | `src/module6_query_intent.py` | `148-165`, `215-236` |
| Module 6 aspect sentiment | `src/module6_aspect_sentiment.py` | `148-154`, `202-279` |
| Module 6 reranker/fallback | `src/module6_reranker.py` | `272-377` |
| Benchmark Module 6 | `scripts/evaluate_module6_retrieval.py` | `172-206`, `240-309` |
| Backend API sentiment/RAG | `backend/app.py` | `266-344`, `381-438` |
| Frontend gọi API RAG | `frontend/app.js` | `455-495` |
| Frontend render answer/evidence | `frontend/app.js` | `279-452` |
| Frontend state tránh output cũ | `frontend/app.js` | `10-20`, `600-603` |

---

## 3. Nếu người khác chụp từng slide và hỏi

### Slide 1: NLP & RAG - Phân tích cảm xúc TMĐT

Họ có thể hỏi:

- Đề tài này chính xác là gì?
- NLP và RAG đóng vai trò nào?
- Sản phẩm cuối cùng của project là gì?

Trả lời ngắn:

> Đề tài dùng NLP để phân loại cảm xúc review sản phẩm TMĐT và dùng RAG để hỏi đáp dựa trên review thật. Sản phẩm cuối gồm pipeline xử lý dữ liệu, model sentiment, FAISS retrieval index, RAG answer có citation và web demo 3 tab.

Code/file nên mở:

```text
README.md
backend/app.py
frontend/index.html
src/module2_baseline_sentiment_classification.py
src/module4_retrieve_upgraded.py
```

Nếu hỏi "có gì để chứng minh đã làm end-to-end?":

> Có dữ liệu processed, model `.joblib`, FAISS index, metric CSV, report và web app chạy local.

---

### Slide 2: Quá tải review

Họ có thể hỏi:

- Vì sao cần hệ thống này?
- Nếu đọc thủ công thì có vấn đề gì?
- Bài toán kinh doanh là gì?

Trả lời ngắn:

> Review TMĐT nhiều, ngắn, nhiễu và phân tán theo nhiều vấn đề như giao hàng, chất lượng, đóng gói, sai hàng. Đọc thủ công không hiệu quả. Hệ thống giúp tự động phân loại cảm xúc và truy xuất bằng chứng để người quản lý biết khách hàng đang phàn nàn hoặc khen gì.

Nếu hỏi "đây là bài toán NLP gì?":

> Có hai bài toán NLP chính: text classification cho sentiment và information retrieval/RAG cho hỏi đáp có bằng chứng.

Code/file nên mở:

```text
data/reports/data_summary.json
src/module1_data_layer.py
src/module2_baseline_sentiment_classification.py
src/module4_retrieve_upgraded.py
```

---

### Slide 3: Giải pháp & mục tiêu cốt lõi

Họ có thể hỏi:

- Sentiment classification là gì?
- RAG là gì?
- Hai phần này kết hợp thế nào?

Trả lời ngắn:

> Sentiment classification dự đoán từng review là tiêu cực, trung lập hoặc tích cực. RAG nhận câu hỏi, tìm review liên quan, rồi tạo câu trả lời có citation. Sentiment được dùng như metadata/filter cho RAG, ví dụ khi hỏi về "phàn nàn" thì ưu tiên review tiêu cực.

Nếu hỏi "RAG có generate bằng LLM không?":

> Không. Trong project này generate là template-based/evidence-grounded. Hệ thống không gọi API LLM bên ngoài, chỉ tổng hợp từ review được truy xuất.

Code/file nên mở:

```text
src/module2_baseline_sentiment_classification.py
src/module4_rag_pipeline_upgraded.py
backend/app.py
```

Dòng code:

- Sentiment API: `backend/app.py:423-428`
- RAG API: `backend/app.py:431-438`
- Generate answer: `src/module4_rag_pipeline_upgraded.py:302-341`

---

### Slide 4: Kiến trúc hệ thống end-to-end

Họ có thể hỏi:

- Pipeline chạy theo thứ tự nào?
- Module nào phụ thuộc module nào?
- Output module trước dùng cho module sau ra sao?

Trả lời ngắn:

> Pipeline gồm: Module 1 làm sạch và chuẩn hóa dữ liệu; Module 2 train sentiment model; Module 3 phân tích thống kê; Module 4 build FAISS index và RAG; Module 5 đánh giá/tổng hợp báo cáo; Module 6 thử nghiệm hybrid retrieval; cuối cùng backend/frontend hiển thị demo.

Nếu hỏi "module nào quan trọng nhất?":

> Với đề tài này, Module 2 và Module 4 là lõi: Module 2 tạo model sentiment, Module 4 tạo retrieval/RAG có bằng chứng.

Code/file nên mở:

```text
src/module1_data_layer.py
src/module2_baseline_sentiment_classification.py
src/module4_build_index.py
src/module4_retrieve_upgraded.py
src/module4_rag_pipeline_upgraded.py
src/module6_hybrid_retrieval.py
backend/app.py
```

---

### Slide 5: Nền tảng dữ liệu 82.677

Họ có thể hỏi:

- 82.677 là gì?
- Vì sao trước đó có số 45k?
- Data RAG và data sentiment khác nhau không?
- Category distribution lấy từ đâu?

Trả lời ngắn:

> 82.677 là số documents trong RAG corpus final. Data sentiment dùng để train classifier chỉ có 5.162 review sau dedup, còn RAG corpus dùng kho review lớn hơn để truy xuất bằng chứng. Số 45k là bản artifact/corpus cũ trong quá trình phát triển, không phải bản final.

File chứng minh:

```text
data/reports/data_summary.json
models/module4/module4_index_config.json
models/module4/review_metadata.parquet
data/processed/rag_corpus_module4.csv
```

Dòng/số cần nhớ:

```text
models/module4/module4_index_config.json -> num_documents = 82677
data/reports/data_summary.json -> rag_total_documents = 82677
```

Nếu hỏi "data đã update chưa?":

> Đã update. Corpus final và FAISS metadata đều đồng bộ ở 82.677 documents.

---

### Slide 6: Chuẩn hóa và phân loại dữ liệu

Họ có thể hỏi:

- Làm sạch dữ liệu như thế nào?
- Rating được biến thành sentiment ra sao?
- Vì sao cần chuẩn hóa dữ liệu?

Trả lời ngắn:

> Module 1 chuẩn hóa text, loại dòng rỗng, parse rating, chỉ giữ rating hợp lệ, map rating sang sentiment và chia train/valid/test. Với sentiment, 1-2 sao là negative, 3 sao là neutral, 4-5 sao là positive.

Code nên mở:

```text
src/module1_data_layer.py
```

Dòng code:

- Clean text: `src/module1_data_layer.py:233-248`
- Parse rating: `src/module1_data_layer.py:329-373`
- Split train/valid/test: `src/module1_data_layer.py:454-501`

Nếu hỏi "vì sao mapping rating sang sentiment có thể nhiễu?":

> Vì rating là tín hiệu gián tiếp. Có người cho 5 sao nhưng vẫn phàn nàn nhẹ, hoặc 3 sao có cả khen và chê. Đây là hạn chế của dữ liệu.

---

### Slide 7: Tinh chỉnh dữ liệu đầu vào, dedup

Họ có thể hỏi:

- Dedup là gì?
- Conflict duplicate là gì?
- Vì sao phải loại duplicate?

Trả lời ngắn:

> Dedup là loại review trùng. Conflict duplicate là cùng một nội dung review nhưng rating/sentiment khác nhau. Nếu giữ lại, model có thể học nhãn mâu thuẫn. Vì vậy project tạo report duplicate, loại conflict và giữ một bản đại diện.

Code nên mở:

```text
src/module1_data_layer.py
```

Dòng code:

- Duplicate report: `src/module1_data_layer.py:392-424`
- Loại conflict duplicate: `src/module1_data_layer.py:426-433`
- Số liệu summary: `src/module1_data_layer.py:805-823`

Số liệu cần nhớ:

```text
Raw sentiment rows: 5.971
After dedup: 5.162
Conflict duplicate removed: 46
```

---

### Slide 8: Tối ưu phân loại cảm xúc

Họ có thể hỏi:

- Vì sao Linear SVM tốt nhất?
- Accuracy 0.9329 và macro-F1 0.9098 nghĩa là gì?
- Majority baseline là gì?
- TF-IDF + SVM hoạt động như thế nào?

Trả lời ngắn:

> Nhóm thử majority baseline, Logistic Regression và Linear SVM trên feature TF-IDF. Linear SVM tốt nhất vì đạt test accuracy 0,9329 và macro-F1 0,9098. Macro-F1 quan trọng vì đánh giá đều cả 3 lớp, không bị lớp đông chi phối.

Code nên mở:

```text
src/module2_baseline_sentiment_classification.py
results/module2/metrics_summary.csv
```

Dòng code:

- Metric: `src/module2_baseline_sentiment_classification.py:205-260`
- Logistic pipeline: `src/module2_baseline_sentiment_classification.py:423-449`
- Linear SVM pipeline: `src/module2_baseline_sentiment_classification.py:451-472`
- Chọn best model: `src/module2_baseline_sentiment_classification.py:608-662`
- Save model: `src/module2_baseline_sentiment_classification.py:826-828`

Số liệu cần nhớ:

```text
Majority baseline: accuracy 0,4297; macro-F1 0,2004
Logistic Regression: accuracy 0,9174; macro-F1 0,8940
Linear SVM: accuracy 0,9329; macro-F1 0,9098
```

---

### Slide 9: Dense Retrieval

Họ có thể hỏi:

- Dense retrieval là gì?
- Embedding là gì?
- FAISS index dùng làm gì?
- Tại sao không chỉ dùng keyword search?

Trả lời ngắn:

> Dense retrieval biến query và review thành embedding vector để tìm theo ngữ nghĩa. Nhờ vậy câu "giao hàng chậm", "ship lâu", "vận chuyển trễ" vẫn có thể gần nhau dù khác từ. FAISS giúp tìm top-k vector gần nhất nhanh trên kho review lớn.

Code nên mở:

```text
src/module4_build_index.py
src/module4_retrieve.py
src/module4_retrieve_upgraded.py
```

Dòng code:

- Build passage text: `src/module4_build_index.py:77-94`
- FAISS IndexFlatIP: `src/module4_build_index.py:101-115`
- Load FAISS/model: `src/module4_retrieve.py:50-89`
- Embed query: `src/module4_retrieve.py:96-103`
- Search FAISS: `src/module4_retrieve_upgraded.py:407-413`

Nếu hỏi "IndexFlatIP là gì?":

> IndexFlatIP là FAISS index dùng inner product. Vì embedding được normalize, inner product tương đương cosine similarity.

---

### Slide 10: RAG evidence-grounded

Họ có thể hỏi:

- Evidence-grounded nghĩa là gì?
- Citation dùng để làm gì?
- RAG có hallucination không?
- Vì sao không dùng LLM?

Trả lời ngắn:

> Evidence-grounded nghĩa là câu trả lời chỉ dựa trên review được truy xuất. Citation [1], [2], [3] giúp kiểm chứng câu trả lời bằng review thật. Project không dùng LLM sinh tự do, nên hạn chế hallucination; nếu evidence yếu thì hệ thống trả lời thận trọng.

Code nên mở:

```text
src/module4_rag_pipeline_upgraded.py
frontend/app.js
```

Dòng code:

- Detect issues: `src/module4_rag_pipeline_upgraded.py:176-222`
- Estimate confidence: `src/module4_rag_pipeline_upgraded.py:222-250`
- Build answer text: `src/module4_rag_pipeline_upgraded.py:256-302`
- Generate answer: `src/module4_rag_pipeline_upgraded.py:302-341`
- Render answer/evidence frontend: `frontend/app.js:279-452`

Nếu hỏi "hallucination là gì?":

> Hallucination là khi hệ thống bịa ra thông tin không có trong dữ liệu. Project giảm rủi ro này bằng cách chỉ trả lời từ evidence truy xuất.

---

### Slide 11: Nâng cấp Hybrid Retrieval

Họ có thể hỏi:

- BM25 khác dense retrieval ở đâu?
- Hybrid retrieval là gì?
- RRF là gì?
- Vì sao hybrid tốt hơn?

Trả lời ngắn:

> BM25 mạnh khi query và review trùng keyword; dense retrieval mạnh khi khác từ nhưng cùng nghĩa. Hybrid retrieval gộp hai nguồn này. RRF fusion giúp review có thứ hạng tốt ở cả BM25 và dense được ưu tiên. Vì vậy hybrid bắt tốt hơn cả keyword lẫn ngữ nghĩa.

Code nên mở:

```text
src/module6_hybrid_retrieval.py
src/module6_query_intent.py
src/module6_reranker.py
scripts/evaluate_module6_retrieval.py
```

Dòng code:

- BM25 fallback: `src/module6_hybrid_retrieval.py:29-84`
- BM25 retriever: `src/module6_hybrid_retrieval.py:146-158`
- Dense wrapper: `src/module6_hybrid_retrieval.py:258-285`
- RRF fusion: `src/module6_hybrid_retrieval.py:289-386`
- Benchmark modes: `scripts/evaluate_module6_retrieval.py:172-206`, `240-309`

Nếu hỏi "hit-rate 1.000 có nghĩa là hoàn hảo không?":

> Không. Đây là benchmark nhỏ/proxy để kiểm tra khả năng bắt keyword/aspect. Nó cho thấy hybrid có tiềm năng tốt hơn, nhưng chưa thay thế đánh giá relevance lớn.

---

### Slide 12: Đánh giá Retrieval baseline, Precision@5 = 0.5067

Họ có thể hỏi:

- Precision@5 nghĩa là gì?
- 0.5067 có thấp không?
- Vì sao Precision@5 cao hơn Precision@3?
- Metric này đo gì?

Trả lời ngắn:

> Precision@5 = 0,5067 nghĩa là trên bộ query chấm tay, trung bình trong top 5 review được trả về có khoảng 50,67% review liên quan. Đây là baseline retrieval. Nó chưa cao nhưng đủ cho demo evidence, và là lý do nhóm thử nâng cấp Module 6 bằng hybrid retrieval.

File nên mở:

```text
results/module5/manual_precision_overall.csv
results/module4/retrieval_eval_summary.csv
figures/module5/manual_precision_at_k.png
```

Số liệu:

```text
Precision@3 = 0,4222
Precision@5 = 0,5067
Precision@10 = 0,4867
Số query đánh giá = 15
```

Nếu hỏi "vì sao Precision@5 không cao?":

> Vì review tiếng Việt nhiễu, query có nhiều cách diễn đạt, dense retrieval có thể lấy review cùng chủ đề nhưng sai intent/sentiment. Đây là hạn chế thực tế của retrieval baseline.

---

### Slide 13: Sức mạnh tuyến tính, macro-F1 0.9098

Họ có thể hỏi:

- Vì sao model tuyến tính lại mạnh?
- Có cần deep learning không?
- Macro-F1 khác accuracy thế nào?

Trả lời ngắn:

> Với dữ liệu review ngắn và số lượng vừa phải, TF-IDF + Linear SVM là baseline mạnh. Nó không cần GPU, dễ giải thích và đạt macro-F1 0,9098. Deep learning như PhoBERT có thể tốt hơn trong tương lai nhưng cần tài nguyên và fine-tune kỹ hơn.

Code nên mở:

```text
src/module2_baseline_sentiment_classification.py
results/module2/metrics_summary.csv
figures/module2/model_comparison_macro_f1.png
```

Dòng code:

- TF-IDF + Linear SVM: `src/module2_baseline_sentiment_classification.py:451-472`
- Save best model: `src/module2_baseline_sentiment_classification.py:826-828`

Nếu hỏi "model thật sự là file nào?":

> Model sentiment chính là `models/module2/best_model.joblib`. Trong bản kết quả, best model là Linear SVM.

---

### Slide 14: Label Noise

Họ có thể hỏi:

- Label noise là gì?
- Vì sao rating-derived label có thể sai?
- Lỗi khó nhất của sentiment là gì?

Trả lời ngắn:

> Label noise là nhãn không phản ánh chính xác nội dung thật. Vì project ánh xạ rating sang sentiment, có thể có trường hợp 5 sao nhưng comment vẫn chê hoặc 3 sao vừa khen vừa chê. Lớp neutral khó nhất vì ít dữ liệu và nội dung thường mixed.

File nên mở:

```text
results/module2/linear_svm_classification_report.csv
results/module2/error_analysis_linear_svm.csv
results/module5/error_analysis.md
```

Số liệu:

```text
negative F1 = 0,9426
neutral F1 = 0,8230
positive F1 = 0,9637
```

Nếu hỏi "hạn chế này xử lý sao?":

> Hướng phát triển là tạo nhãn thủ công tốt hơn, dùng ABSA dataset, hoặc fine-tune PhoBERT/XLM-R với dữ liệu chất lượng cao.

---

### Slide 15: Giao diện 3 tab

Họ có thể hỏi:

- Vì sao tách 3 tab?
- Tab sentiment và RAG khác nhau thế nào?
- Backend/frontend hoạt động ra sao?

Trả lời ngắn:

> Tách 3 tab để tránh nhầm lẫn. Tab Sentiment phân tích một review thật. Tab RAG hỏi đáp trên kho review. Tab Kỹ thuật & đánh giá hiển thị corpus, model, index và metric. Backend FastAPI cung cấp API; frontend gọi API và render answer/evidence.

Code nên mở:

```text
backend/app.py
frontend/index.html
frontend/app.js
frontend/styles.css
```

Dòng code:

- API health/config: `backend/app.py:381-420`
- API sentiment: `backend/app.py:423-428`
- API RAG: `backend/app.py:431-438`
- Frontend gọi API RAG: `frontend/app.js:455-495`
- Render answer/evidence: `frontend/app.js:279-452`

Nếu hỏi "tại sao câu hỏi RAG không đưa qua sentiment model?":

> Vì câu hỏi RAG không phải review sản phẩm. Sentiment tab chỉ dùng cho review thật. Trong RAG, hệ thống dùng intent/aspect detector và metadata filter, không gọi đó là phân tích sentiment câu hỏi.

---

### Slide 16: Tối ưu trải nghiệm người dùng

Họ có thể hỏi:

- UI có xử lý loading/error/empty state không?
- Làm sao tránh output cũ không khớp query mới?
- Evidence card hiển thị gì?

Trả lời ngắn:

> Frontend có state management: lưu `lastRunQuery`, hiển thị cảnh báo nếu người dùng sửa query sau khi đã chạy nhưng chưa bấm chạy lại. Output RAG luôn ghi rõ kết quả cho câu hỏi nào. Evidence card hiển thị citation, điểm liên quan, ngành hàng, số sao, sentiment và excerpt review.

Code nên mở:

```text
frontend/app.js
frontend/styles.css
```

Dòng code:

- State: `frontend/app.js:10-20`
- Loading/error state: `frontend/app.js:131-147`, `438-495`
- Render evidence card: `frontend/app.js:341-412`
- Cảnh báo query thay đổi: `frontend/app.js:600-603`

---

### Slide 17: Chuyển hóa AI thành lợi nhuận

Họ có thể hỏi:

- Hệ thống này có ý nghĩa kinh doanh gì?
- Người bán dùng được gì từ kết quả?
- Nó giúp ra quyết định ra sao?

Trả lời ngắn:

> Hệ thống giúp người bán/nhà quản lý nắm nhanh vấn đề khách hàng đang gặp: giao hàng, chất lượng, đóng gói, sai hàng, thiếu hàng, phản hồi shop. Từ đó có thể ưu tiên cải thiện vận hành, logistics, mô tả sản phẩm hoặc chăm sóc khách hàng.

Không nên nói:

> Hệ thống chắc chắn tăng lợi nhuận.

Nên nói:

> Hệ thống cung cấp insight có bằng chứng để hỗ trợ quyết định, còn tác động kinh doanh cần đo bằng dữ liệu vận hành thực tế.

File nên mở:

```text
results/module3/top_negative_reviews.csv
results/module4/rag_outputs.md
results/module5/final_discussion.md
```

---

### Slide 18: Hạn chế và tương lai LLM

Họ có thể hỏi:

- Vì sao chưa dùng LLM?
- Tương lai nâng cấp thế nào?
- LLM có thay thế template không?
- Deep learning/ABSA/reranker là gì?

Trả lời ngắn:

> Hiện tại project không dùng LLM để tránh phụ thuộc API và hạn chế hallucination. Hướng phát triển là tích hợp LLM có kiểm soát citation, fine-tune PhoBERT/XLM-R cho sentiment, xây dựng ABSA dataset và huấn luyện reranker supervised.

Nếu hỏi "LLM có tốt hơn không?":

> Có thể giúp câu trả lời tự nhiên hơn, nhưng cần ràng buộc evidence/citation để không bịa. Trong đề tài này, template-based generation phù hợp hơn vì dễ kiểm soát và giải thích.

File nên mở:

```text
results/module5/final_discussion.md
results/module5/final_conclusion.md
README_MODULE6.md
```

---

### Slide 19: Tổng kết hành trình RAG

Họ có thể hỏi:

- Project đã hoàn thành gì?
- Kết quả nổi bật là gì?
- Hạn chế là gì?
- Nếu làm tiếp thì làm gì?

Trả lời ngắn:

> Project hoàn thành pipeline end-to-end: xử lý dữ liệu, train sentiment model, phân tích review, build RAG index, trả lời có evidence và web demo. Kết quả nổi bật là Linear SVM đạt macro-F1 0,9098 và RAG final dùng 82.677 documents. Hạn chế là label từ rating có nhiễu, retrieval Precision@5 còn baseline và RAG chưa dùng LLM thật.

Kết luận nên nói:

> Đề tài chứng minh được hướng kết hợp sentiment classification và RAG để phân tích review TMĐT có bằng chứng, nhưng vẫn còn không gian nâng cấp về dữ liệu, reranking và LLM có kiểm soát citation.

---

## 4. Nếu họ chụp giao diện web và hỏi

### Câu hỏi: "Tại sao có 3 tab?"

Trả lời:

> Vì sentiment và RAG là hai tác vụ khác nhau. Sentiment tab phân tích một review cụ thể. RAG tab trả lời câu hỏi trên kho review. Tab kỹ thuật hiển thị model, corpus, FAISS index và metric.

Code:

```text
frontend/index.html
frontend/app.js:147-155
```

### Câu hỏi: "Score trong evidence là gì?"

Trả lời:

> Score là điểm liên quan từ retrieval/rerank. Với dense retrieval, score đến từ similarity giữa query embedding và review embedding. Ở bản nâng cấp, rerank_score còn kết hợp dense score, keyword score và aspect score.

Code:

```text
src/module4_retrieve_upgraded.py:407-452
frontend/app.js:75-80
frontend/app.js:341-412
```

### Câu hỏi: "Confidence trong answer là gì?"

Trả lời:

> Confidence trong UI là heuristic dựa trên evidence hiện tại, ví dụ số review dùng được, score trung bình và số issue phát hiện. Nó không thay thế metric Precision@k trong báo cáo.

Code:

```text
src/module4_rag_pipeline_upgraded.py:222-250
frontend/app.js:310-315
```

### Câu hỏi: "Tại sao có debug panel?"

Trả lời:

> Debug panel giúp kiểm tra query gốc, query expanded, filter, model, paths và số candidate/returned. Nó phục vụ minh bạch kỹ thuật khi demo.

Code:

```text
frontend/app.js:413-437
backend/app.py:344-364
```

---

## 5. Nếu họ chụp JSON/config và hỏi

### `models/module4/module4_index_config.json`

Có thể hỏi:

- `num_documents` là gì?
- `embedding_model` là gì?
- `IndexFlatIP` là gì?
- `e5_query_prefix` và `e5_passage_prefix` là gì?

Trả lời:

> File này là config của FAISS index final. Nó cho biết index dùng 82.677 documents, embedding model `intfloat/multilingual-e5-small`, embedding dimension 384, index type `IndexFlatIP`, và prefix E5 cho query/passage.

### `data/reports/data_summary.json`

Có thể hỏi:

- Sentiment data và RAG data khác nhau không?
- Vì sao sentiment chỉ 5.162 mà RAG 82.677?

Trả lời:

> Sentiment data là tập có label để train classifier. RAG data là kho review lớn hơn để truy xuất evidence. Hai tập phục vụ hai mục tiêu khác nhau.

### `results/module2/metrics_summary.csv`

Có thể hỏi:

- Model nào tốt nhất?
- Dựa vào metric nào?

Trả lời:

> Linear SVM tốt nhất, chọn theo validation macro-F1. Trên test, nó đạt accuracy 0,9329 và macro-F1 0,9098.

### `results/module5/manual_precision_overall.csv`

Có thể hỏi:

- Precision@3/5/10 là gì?
- Tại sao phải chấm tay?

Trả lời:

> Retrieval cần biết review trả về có liên quan query không. Việc này không thể chỉ dựa vào rating/sentiment, nên cần chấm relevance thủ công cho bộ query đánh giá. Precision@k đo tỷ lệ review liên quan trong top-k.

---

## 6. Nếu họ chụp source code và hỏi dòng đó làm gì

### Code TF-IDF + Logistic Regression

File:

```text
src/module2_baseline_sentiment_classification.py:423-449
```

Trả lời:

> Đoạn này tạo pipeline gồm TfidfVectorizer và LogisticRegression. TfidfVectorizer biến review thành vector n-gram, LogisticRegression học trọng số để phân loại sentiment.

### Code TF-IDF + Linear SVM

File:

```text
src/module2_baseline_sentiment_classification.py:451-472
```

Trả lời:

> Đoạn này tạo pipeline TF-IDF + LinearSVC. LinearSVC phù hợp với dữ liệu text sparse và là model đạt kết quả tốt nhất trong project.

### Code chọn best model

File:

```text
src/module2_baseline_sentiment_classification.py:608-662
```

Trả lời:

> Đoạn này so sánh các model theo validation macro-F1, chọn model tốt nhất rồi lưu thông tin kết quả.

### Code build FAISS index

File:

```text
src/module4_build_index.py:77-115
```

Trả lời:

> Đoạn này encode toàn bộ `retrieval_text` bằng multilingual-E5 với prefix `passage:`, normalize embedding, tạo FAISS IndexFlatIP, add vector vào index, rồi lưu index và metadata.

### Code retrieve FAISS

File:

```text
src/module4_retrieve_upgraded.py:387-459
```

Trả lời:

> Đoạn này nhận query, tự suy luận sentiment filter nếu bật auto filter, expand query, encode query, search FAISS, lọc metadata theo category/sentiment/rating, tính keyword/aspect score rồi sort theo rerank_score.

### Code generate answer

File:

```text
src/module4_rag_pipeline_upgraded.py:302-341
```

Trả lời:

> Đoạn này nhận evidence đã retrieve, phát hiện vấn đề chính, ước lượng độ tin cậy, build evidence items và tạo câu trả lời có citation.

### Code Module 6 hybrid

File:

```text
src/module6_hybrid_retrieval.py:297-386
```

Trả lời:

> Đoạn này gộp kết quả BM25 và dense retrieval bằng RRF. Mỗi review có thể có điểm từ BM25 và dense; RRF giúp ưu tiên review có thứ hạng tốt ở nhiều nguồn.

### Code backend RAG API

File:

```text
backend/app.py:431-438
```

Trả lời:

> Đây là endpoint `/api/rag`. Nó nhận request từ frontend, chạy retrieval, generate answer, build understanding/technical details rồi trả JSON cho giao diện.

### Code frontend gọi RAG

File:

```text
frontend/app.js:455-495
```

Trả lời:

> Đây là hàm chạy khi bấm nút Chạy RAG. Nó lấy payload từ form, kiểm tra query rỗng, gọi API `/api/rag`, rồi render kết quả hoặc error.

---

## 7. Câu hỏi khó và câu trả lời an toàn

### "Tại sao không dùng PhoBERT ngay từ đầu?"

Trả lời:

> Vì mục tiêu ban đầu là xây dựng baseline end-to-end ổn định và dễ giải thích. Với dữ liệu sentiment 5.162 review, TF-IDF + Linear SVM đã đạt macro-F1 0,9098. PhoBERT/XLM-R là hướng phát triển tiếp theo nếu có thêm thời gian và tài nguyên fine-tune.

### "Nếu label lấy từ rating thì có đáng tin không?"

Trả lời:

> Đây là hạn chế. Rating-derived label giúp tạo nhãn nhanh khi không có annotation thủ công, nhưng có nhiễu. Project đã ghi rõ hạn chế này và có error analysis, đặc biệt neutral/mixed là lớp khó.

### "RAG trả lời có thể sai không?"

Trả lời:

> Có thể, nếu retrieval lấy evidence không liên quan hoặc query quá chung. Vì vậy hệ thống hiển thị evidence card và citation để người dùng kiểm chứng. Khi evidence yếu, hệ thống nên trả lời thận trọng.

### "Precision@5 chỉ 0,5067 thì có dùng được không?"

Trả lời:

> Đây là baseline retrieval trên bộ đánh giá nhỏ. Nó cho thấy hệ thống đã lấy được evidence liên quan ở mức nhất định nhưng chưa hoàn hảo. Chính vì vậy project có Module 6 để cải thiện retrieval bằng hybrid BM25 + dense + rerank.

### "Module 6 benchmark 1.000 có mâu thuẫn với Precision@5 0,5067 không?"

Trả lời:

> Không. Precision@5 là manual relevance evaluation cho Module 4 baseline trên 15 query. Module 6 benchmark là proxy nhỏ, handcrafted, đo keyword/aspect hit-rate để so sánh phương pháp retrieval. Hai metric đo hai việc khác nhau.

### "RAG có thật sự là RAG nếu không dùng LLM?"

Trả lời:

> Có thể gọi là RAG-style/evidence-grounded RAG pipeline vì có bước retrieve evidence và generate câu trả lời từ evidence. Tuy nhiên project không dùng LLM sinh tự do; phần generate là template-based. Em sẽ mô tả chính xác là RAG-style evidence-grounded answer generation.

### "Nếu dữ liệu RAG 82.677 có rating missing nhiều thì sao?"

Trả lời:

> Rating có thể thiếu trong một phần corpus, nhưng RAG vẫn dùng comment/retrieval_text, category và predicted_sentiment để truy xuất. Khi cần filter rating thì chỉ áp dụng trên bản ghi có rating hợp lệ.

### "Tại sao không chấm tự động relevance thay vì manual?"

Trả lời:

> Relevance giữa query và review là đánh giá ngữ nghĩa. Nếu tự chấm bằng keyword hoặc sentiment thì dễ sai. Manual evaluation nhỏ giúp có baseline đáng tin hơn. Về sau có thể mở rộng bằng bộ query lớn hơn hoặc dùng LLM judge có kiểm soát, nhưng cần kiểm chứng.

---

## 8. Những câu mở đầu khi show code

Khi mở Module 1:

> Đây là code xử lý dữ liệu. Em muốn chứng minh pipeline không chỉ train model mà có bước làm sạch, dedup, mapping label và split dữ liệu.

Khi mở Module 2:

> Đây là code train sentiment model. Em dùng pipeline TF-IDF + classifier, thử Logistic Regression và Linear SVM, sau đó chọn model theo validation macro-F1.

Khi mở Module 4:

> Đây là code RAG. Phần này load FAISS index, encode query bằng E5, retrieve review, áp dụng filter và tạo câu trả lời có citation.

Khi mở Module 6:

> Đây là hướng nâng cấp retrieval. Em kết hợp BM25 để bắt keyword và dense retrieval để bắt ngữ nghĩa, rồi dùng RRF/rerank để hợp nhất kết quả.

Khi mở backend/frontend:

> Đây là phần demo sản phẩm. Backend cung cấp API, frontend gọi API và render thành các tab sentiment, RAG và kỹ thuật.

---

## 9. Câu trả lời siêu ngắn theo keyword

| Nếu bị hỏi | Trả lời nhanh |
|---|---|
| NLP là gì? | Xử lý ngôn ngữ tự nhiên, giúp máy tính xử lý review tiếng Việt. |
| Sentiment là gì? | Phân loại cảm xúc review: negative, neutral, positive. |
| TF-IDF là gì? | Biến text thành vector dựa trên độ quan trọng của từ. |
| SVM là gì? | Model tuyến tính tìm ranh giới phân tách các lớp. |
| Macro-F1 là gì? | Trung bình F1 của từng lớp, công bằng với lớp ít dữ liệu. |
| Embedding là gì? | Vector biểu diễn ý nghĩa của câu/review. |
| multilingual-E5 là gì? | Model embedding đa ngôn ngữ dùng cho query/passage retrieval. |
| FAISS là gì? | Thư viện tìm kiếm vector nhanh. |
| RAG là gì? | Retrieve evidence rồi generate answer dựa trên evidence. |
| Citation là gì? | Dẫn chứng review [1], [2], [3] để kiểm chứng câu trả lời. |
| BM25 là gì? | Retrieval theo keyword. |
| Dense retrieval là gì? | Retrieval theo vector/ngữ nghĩa. |
| RRF là gì? | Cách gộp nhiều ranking. |
| Module 6 là gì? | Nâng cấp retrieval bằng BM25 + Dense + RRF/rerank + aspect rules. |
| Precision@5 là gì? | Tỷ lệ review liên quan trong top 5 kết quả. |
| Vì sao không dùng LLM? | Để tránh phụ thuộc API và hạn chế hallucination trong phạm vi đề tài. |

---

## 10. Checklist cuối trước khi lên trình bày

Mở sẵn các tab/file:

- Web app: `http://127.0.0.1:8000`
- GitHub repo: `https://github.com/AlizCuli/Vietnamese-Ecommerce-Sentiment-RAG`
- `PROJECT_THUYET_TRINH_VA_QA.md`
- `PRESENTATION_SCREENSHOT_QA_CODE_MAP.md`
- `data/reports/data_summary.json`
- `models/module4/module4_index_config.json`
- `results/module2/metrics_summary.csv`
- `results/module5/manual_precision_overall.csv`
- `src/module2_baseline_sentiment_classification.py`
- `src/module4_retrieve_upgraded.py`
- `src/module4_rag_pipeline_upgraded.py`
- `backend/app.py`

Test trước:

```powershell
cd "C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted"
python scripts\run_rag_webapp.py
```

Mở:

```text
http://127.0.0.1:8000
```

Query demo nên dùng:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
Có review nào nói hàng bị lỗi hoặc hỏng không?
Khách hàng chê chất lượng sản phẩm ở điểm nào?
Review nào nói shop giao thiếu hàng?
```

