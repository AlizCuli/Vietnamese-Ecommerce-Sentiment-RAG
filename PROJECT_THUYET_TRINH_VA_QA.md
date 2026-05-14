# Sổ tay thuyết trình và hỏi đáp project NLP + Sentiment + RAG

Tài liệu này dùng để nắm toàn bộ project trước khi thuyết trình. Nội dung được viết theo hướng dễ nói, dễ nhớ, nhưng vẫn đủ kỹ thuật để trả lời khi giảng viên hoặc các bạn hỏi sâu.

Đề tài:

**Ứng dụng Xử lý ngôn ngữ tự nhiên và Retrieval-Augmented Generation trong phân tích cảm xúc đánh giá sản phẩm thương mại điện tử**

Đường dẫn project final:

```text
C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted
```

GitHub:

```text
https://github.com/AlizCuli/Vietnamese-Ecommerce-Sentiment-RAG
```

---

## 1. Nói cực ngắn về project

Project xây dựng một hệ thống phân tích review TMĐT tiếng Việt gồm hai phần chính:

1. **Sentiment Classification**: dự đoán một review là tiêu cực, trung lập hay tích cực.
2. **RAG Review Insight**: người dùng đặt câu hỏi, hệ thống truy xuất các review liên quan rồi tạo câu trả lời có bằng chứng/citation.

Nói đơn giản:

> Hệ thống không chỉ nói review tốt hay xấu, mà còn giúp hỏi: "Khách hàng đang phàn nàn điều gì?", sau đó trả lời dựa trên review thật.

---

## 2. Bài toán project giải quyết

Trong thương mại điện tử, mỗi sản phẩm hoặc ngành hàng có rất nhiều review. Nếu đọc thủ công thì mất thời gian. Người bán hoặc người quản lý muốn biết:

- Khách hàng đang khen/chê gì?
- Review nào là tiêu cực?
- Vấn đề giao hàng, đóng gói, sai hàng, thiếu hàng, size, chất lượng nằm ở đâu?
- Có bằng chứng cụ thể từ review không?

Project xử lý bằng NLP:

- Biến review tiếng Việt thành dữ liệu máy học.
- Huấn luyện model sentiment.
- Xây dựng kho truy xuất review bằng embedding và FAISS.
- Tạo giao diện web để demo sentiment và RAG.

---

## 3. Input và output của hệ thống

### Input

Input chính gồm:

- Dữ liệu review sản phẩm TMĐT tiếng Việt.
- Review có các trường như comment, rating, product_name, category/domain, sentiment.
- Câu hỏi từ người dùng, ví dụ:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
Có review nào nói shop giao thiếu hàng?
Khách hàng chê chất lượng sản phẩm ở điểm nào?
```

### Output

Output gồm:

- Nhãn sentiment cho một review: tiêu cực, trung lập, tích cực.
- Bảng thống kê sentiment.
- Top review tiêu cực.
- Kết quả RAG:
  - Tóm tắt câu trả lời.
  - Các vấn đề chính.
  - Review bằng chứng với citation [1], [2], [3].
  - Độ tin cậy.
  - Chi tiết kỹ thuật nếu cần kiểm tra.

---

## 4. Cấu trúc thư mục cần nhớ

| Thư mục/file | Vai trò |
|---|---|
| `data/` | Chứa dữ liệu đầu vào, dữ liệu đã xử lý, query đánh giá và summary dữ liệu. |
| `src/` | Code chính của các module 1 đến 6. |
| `models/` | Chứa model sentiment và FAISS index/metadata cho RAG. |
| `results/` | Chứa metric, output đánh giá, error analysis và kết quả RAG. |
| `figures/` | Chứa hình biểu đồ cho báo cáo. |
| `backend/` | FastAPI backend cho web demo. |
| `frontend/` | HTML/CSS/JS của giao diện web. |
| `scripts/` | Script chạy module, chạy web app, đánh giá Module 6. |
| `report_latex/` | Báo cáo LaTeX. |
| `README_MODULE*.md` | Giải thích từng module. |
| `README_RAG_WEBAPP.md` | Hướng dẫn web app. |

---

## 5. Luồng xử lý tổng thể

```text
Raw review data
   ↓
Module 1: Data Layer
   - Làm sạch text
   - Xử lý duplicate
   - Mapping rating sang sentiment
   - Chia train/valid/test
   - Tạo corpus RAG
   ↓
Module 2: Sentiment Classification
   - TF-IDF
   - Logistic Regression
   - Linear SVM
   - Chọn model tốt nhất bằng validation macro-F1
   ↓
Module 3: Review Analytics
   - Thống kê sentiment
   - Crosstab rating-sentiment
   - Top negative reviews
   - Biểu đồ
   ↓
Module 4: Retrieval/RAG
   - Encode review bằng multilingual-E5
   - Build FAISS index
   - Retrieve top-k review liên quan
   - Tạo câu trả lời có citation
   ↓
Module 5: Evaluation & Report
   - Tổng hợp metric
   - Manual Precision@k
   - Error analysis
   ↓
Module 6: Hybrid Retrieval Enhancement
   - BM25 + Dense FAISS + RRF/rerank
   - Aspect-aware rules
   ↓
Web Demo
   - Tab Sentiment
   - Tab RAG
   - Tab Kỹ thuật & đánh giá
```

---

## 6. Data của project

### 6.1. Data sentiment

Số liệu chính:

| Chỉ số | Giá trị |
|---|---:|
| Raw rows | 5.971 |
| Sau làm sạch | 5.971 |
| Sau dedup | 5.162 |
| Conflict duplicate bị loại | 46 |

Phân phối sentiment 3 lớp:

| Sentiment | Số lượng |
|---|---:|
| Positive | 2.217 |
| Negative | 2.074 |
| Neutral | 871 |

Phân phối rating:

| Rating | Số lượng |
|---|---:|
| 1 sao | 1.079 |
| 2 sao | 995 |
| 3 sao | 871 |
| 4 sao | 794 |
| 5 sao | 1.423 |

Quy tắc mapping:

| Rating | Sentiment |
|---|---|
| 1-2 sao | Negative |
| 3 sao | Neutral |
| 4-5 sao | Positive |

Chia tập train/valid/test:

| Split | Negative | Neutral | Positive |
|---|---:|---:|---:|
| Train | 1.452 | 609 | 1.552 |
| Valid | 311 | 131 | 332 |
| Test | 311 | 131 | 333 |

Nói đơn giản:

> Data sentiment dùng để huấn luyện model phân loại cảm xúc từng review.

### 6.2. Data RAG

Final RAG corpus:

| Chỉ số | Giá trị |
|---|---:|
| Tổng documents final | 82.677 |
| Embedding model | `intfloat/multilingual-e5-small` |
| Embedding dimension | 384 |
| FAISS index | `IndexFlatIP` |
| Similarity | cosine similarity qua normalized inner product |

File chính:

| File | Vai trò |
|---|---|
| `data/processed/rag_corpus_module4.csv` | Corpus RAG final 82.677 documents. |
| `models/module4/review_metadata.parquet` | Metadata review dùng khi trả evidence. |
| `models/module4/review_faiss.index` | Vector index để tìm review gần nhất. |
| `models/module4/module4_index_config.json` | Config xác nhận số documents, model embedding, index type. |

Phân phối category trong RAG final:

| Category | Số lượng |
|---|---:|
| Fashion | 24.989 |
| Electronic | 19.645 |
| HealthBeauty | 13.739 |
| BabiesToys | 10.827 |
| HomeLifestyle | 9.798 |
| App | 1.978 |
| Cosmetic | 1.262 |
| Mobile | 439 |

### 6.3. Nếu bị hỏi: "Ban đầu data chỉ khoảng 42k/45k, sao giờ 82.677?"

Trả lời:

> Ban đầu project có một bản RAG corpus/index cũ khoảng hơn 45k documents. Sau đó nhóm đã gộp thêm dữ liệu RAG từ nguồn bổ sung và build lại artifact final. Bản final đang dùng trong demo và báo cáo là 82.677 documents, được xác nhận trong `models/module4/module4_index_config.json`, `data/reports/data_summary.json` và `models/module4/review_metadata.parquet`.

Điểm quan trọng:

- Không nói 45k là bản final.
- Nếu ai hỏi số nào đúng: **82.677 là số final**.
- 42k/45k chỉ là bản trung gian/cũ trong quá trình phát triển.

---

## 7. Module 1: Data Layer

File chính:

```text
src/module1_data_layer.py
```

Module này làm gì:

- Đọc dữ liệu review.
- Chuẩn hóa text.
- Chuẩn hóa rating.
- Mapping rating sang sentiment.
- Xử lý duplicate.
- Chia train/valid/test.
- Tạo các file processed cho module sau.

Nói đơn giản:

> Module 1 là tầng chuẩn bị dữ liệu. Nếu dữ liệu bẩn thì model phía sau học sai, nên bước này rất quan trọng.

Vì sao cần làm sạch?

- Review có thể thiếu text.
- Review có thể trùng.
- Có review cùng text nhưng rating/sentiment mâu thuẫn.
- Text tiếng Việt có thể thừa khoảng trắng, ký tự lạ, HTML.

Vì sao cần chia train/valid/test?

- Train: để model học.
- Valid: để chọn model/hyperparameter tốt nhất.
- Test: để đánh giá cuối cùng, tránh tự lừa mình bằng kết quả trên data đã dùng chọn model.

Câu hỏi thường gặp:

**Hỏi: Vì sao không train trên toàn bộ data?**

Trả lời:

> Nếu train trên toàn bộ data thì không còn tập độc lập để kiểm tra model. Chia train/valid/test giúp đánh giá khách quan hơn.

**Hỏi: Duplicate có ảnh hưởng gì?**

Trả lời:

> Nếu cùng một review xuất hiện nhiều lần, model có thể học lệch hoặc test bị trùng với train. Đặc biệt conflict duplicate là trường hợp cùng text nhưng label khác, dễ làm nhiễu nhãn.

---

## 8. Module 2: Sentiment Classification

File chính:

```text
src/module2_baseline_sentiment_classification.py
```

Mục tiêu:

> Huấn luyện model phân loại review thành negative, neutral, positive.

Các phương pháp:

1. Majority baseline.
2. TF-IDF + Logistic Regression.
3. TF-IDF + Linear SVM.

### 8.1. TF-IDF là gì?

TF-IDF là cách biến văn bản thành vector số.

Ý tưởng:

- Từ xuất hiện nhiều trong một review thì quan trọng.
- Nhưng nếu từ đó xuất hiện ở hầu hết mọi review, nó không còn đặc biệt.

Ví dụ:

Review A:

```text
shop giao hàng chậm, sản phẩm bị lỗi
```

Các từ như `chậm`, `lỗi` có thể quan trọng hơn các từ phổ biến như `shop`, `sản phẩm`.

Nói đơn giản:

> TF-IDF giúp model biết review có những từ khóa nào nổi bật.

### 8.2. Logistic Regression là gì?

Logistic Regression là model phân loại tuyến tính. Nó học trọng số cho từng feature TF-IDF.

Ví dụ:

- Từ `lỗi`, `hỏng`, `tệ`, `không dùng được` có trọng số nghiêng về negative.
- Từ `tốt`, `đẹp`, `ưng`, `nhanh` có trọng số nghiêng về positive.

### 8.3. Linear SVM là gì?

Linear SVM là model tìm đường phân cách tốt giữa các lớp trong không gian vector.

Vì sao hợp với text?

- Text TF-IDF tạo vector rất nhiều chiều.
- Linear SVM thường mạnh với dữ liệu sparse, nhiều feature.
- Nó hoạt động tốt với bài toán phân loại văn bản truyền thống.

### 8.4. Majority baseline là gì?

Baseline đơn giản nhất: luôn đoán lớp xuất hiện nhiều nhất.

Trong project, lớp nhiều nhất là positive, nên majority baseline chủ yếu đoán positive.

Ý nghĩa:

> Baseline cho biết nếu không dùng model thông minh thì điểm thấp thế nào. Model tốt phải vượt baseline rõ ràng.

### 8.5. Kết quả Module 2

| Model | Test Accuracy | Test Macro-F1 | Test Weighted-F1 |
|---|---:|---:|---:|
| Majority baseline | 0,4297 | 0,2004 | 0,2583 |
| Logistic Regression | 0,9174 | 0,8940 | 0,9176 |
| Linear SVM | 0,9329 | 0,9098 | 0,9315 |

Model tốt nhất:

> Linear SVM, vì có validation macro-F1 tốt nhất và test macro-F1 đạt 0,9098.

Per-class F1 của Linear SVM:

| Lớp | F1-score |
|---|---:|
| Negative | 0,9426 |
| Neutral | 0,8230 |
| Positive | 0,9637 |

Điểm yếu:

> Neutral thấp hơn negative và positive vì lớp neutral ít dữ liệu hơn và nhiều review 3 sao có nội dung lẫn khen/chê.

### 8.6. Metric cần hiểu

Accuracy:

> Tỷ lệ dự đoán đúng trên toàn bộ mẫu.

Precision:

> Trong những mẫu model đoán là một lớp, có bao nhiêu mẫu thật sự đúng lớp đó.

Recall:

> Trong những mẫu thật sự thuộc một lớp, model tìm đúng được bao nhiêu.

F1-score:

> Trung bình điều hòa giữa precision và recall.

Macro-F1:

> Tính F1 từng lớp rồi lấy trung bình, không thiên vị lớp đông dữ liệu.

Weighted-F1:

> Tính F1 theo trọng số số lượng mẫu từng lớp.

Nếu bị hỏi vì sao chọn macro-F1:

> Vì data có lệch lớp, neutral ít hơn positive/negative. Macro-F1 buộc model phải làm tốt trên cả lớp ít dữ liệu, không chỉ tối ưu lớp đông.

---

## 9. Module 3: Review Analytics

Module này không huấn luyện model mới.

Nó dùng kết quả sentiment và dữ liệu review để phân tích:

- Phân phối sentiment.
- Phân phối rating.
- Bảng rating-sentiment.
- Top negative reviews.
- Biểu đồ cho báo cáo.

File kết quả thường xem:

```text
results/module3/overall_sentiment_distribution.csv
results/module3/rating_sentiment_crosstab.csv
results/module3/top_negative_reviews.csv
figures/module3/
```

Nói đơn giản:

> Module 3 biến kết quả model thành insight thống kê để hiểu dữ liệu.

Nếu bị hỏi Module 3 có train không:

> Không. Module 3 là analytics, không phải training. Nó thống kê và trực quan hóa kết quả.

---

## 10. Module 4: Retrieval và RAG

Các file chính:

```text
src/module4_prepare_inputs.py
src/module4_build_index.py
src/module4_retrieve.py
src/module4_retrieve_upgraded.py
src/module4_rag_pipeline.py
src/module4_rag_pipeline_upgraded.py
src/module4_evaluate.py
```

Artifact chính:

```text
models/module4/review_faiss.index
models/module4/review_metadata.parquet
models/module4/module4_index_config.json
```

### 10.1. Retrieval là gì?

Retrieval là tìm các tài liệu liên quan nhất đến câu hỏi.

Ví dụ:

Query:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
```

Hệ thống phải tìm các review nói về:

- giao hàng lâu,
- ship chậm,
- vận chuyển trễ,
- nhận hàng muộn,
- xử lý đơn chậm.

### 10.2. Embedding là gì?

Embedding là vector số biểu diễn ý nghĩa của câu.

Ví dụ:

```text
giao hàng chậm
ship lâu
vận chuyển trễ
```

Ba câu này có từ khác nhau nhưng ý nghĩa gần nhau. Embedding giúp chúng nằm gần nhau trong không gian vector.

### 10.3. multilingual-E5 là gì?

Project dùng:

```text
intfloat/multilingual-e5-small
```

Đây là model embedding đa ngôn ngữ. Nó biến query và review thành vector 384 chiều.

E5 yêu cầu prefix:

```text
query: câu hỏi người dùng
passage: nội dung review
```

Vì sao cần prefix?

> E5 được train theo format query/passage. Dùng đúng prefix giúp embedding ổn định hơn.

### 10.4. FAISS index là gì?

FAISS là thư viện tìm kiếm vector nhanh.

Thay vì so query với từng review một cách chậm, FAISS lưu toàn bộ vector review trong index để tìm top-k nhanh hơn.

Project dùng:

```text
IndexFlatIP
```

Vì embedding được normalize, inner product tương đương cosine similarity.

### 10.5. RAG trong project này là gì?

RAG = Retrieve + Generate.

Trong project:

1. Retrieve: tìm review liên quan bằng FAISS.
2. Generate: tạo câu trả lời dựa trên review tìm được.

Điểm cực kỳ quan trọng:

> Project không dùng LLM thật như ChatGPT/Gemini để sinh tự do. Phần generate là template-based/evidence-grounded, tức chỉ tổng hợp từ evidence đã truy xuất.

Nếu bị hỏi:

**Hỏi: RAG của bạn có dùng LLM không?**

Trả lời:

> Không dùng LLM bên ngoài. Hệ thống dùng retrieval để lấy review thật, sau đó sinh câu trả lời theo template có citation. Cách này an toàn hơn trong phạm vi project vì tránh bịa nội dung ngoài dữ liệu.

### 10.6. Output RAG gồm gì?

Output gồm:

- Câu hỏi đã chạy.
- Hệ thống hiểu câu hỏi như thế nào.
- Aspect/chủ đề nhận diện.
- Sentiment filter.
- Query expansion.
- Câu trả lời có bằng chứng.
- Review evidence [1], [2], [3].
- Độ tin cậy.
- Debug kỹ thuật nếu cần.

Ví dụ câu hỏi:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
```

Answer nên nói:

```text
Trong các review được truy xuất, khách hàng chủ yếu phàn nàn về giao hàng chậm,
giao sai hoặc thiếu hàng, và phản hồi hỗ trợ chưa tốt. Các nhận định này dựa
trên review [1], [2], [3].
```

### 10.7. Precision@5 là gì?

Manual Precision@5 của Module 4:

```text
0,5067
```

Ý nghĩa:

> Trung bình trong top 5 review hệ thống trả về, khoảng 50,67% review được chấm là liên quan.

Nói dễ hiểu:

> Với mỗi câu hỏi, nếu hệ thống trả 5 review, thì trung bình khoảng 2-3 review thật sự liên quan.

Nếu bị hỏi: "Tại sao Precision@5 chỉ 0,5067 mà app lại có độ tin cậy cao?"

Trả lời:

> Precision@5 là metric baseline đánh giá retrieval trên 15 query thủ công. Còn độ tin cậy trong app là heuristic theo kết quả hiện tại, ví dụ score cao, sentiment/category phù hợp và evidence có keyword/aspect liên quan. Hai chỉ số đo hai việc khác nhau. Khi thuyết trình, em sẽ nói rõ Precision@5 là baseline retrieval còn confidence trong UI chỉ là tín hiệu hỗ trợ, không phải metric học thuật thay thế.

---

## 11. Module 5: Evaluation và Report

File chính:

```text
src/module5_collect_results.py
src/module5_error_analysis.py
src/module5_generate_figures.py
src/module5_generate_report_sections.py
src/module5_manual_retrieval_eval.py
```

Module này làm gì:

- Gom kết quả từ các module.
- Tạo bảng metric.
- Tạo error analysis.
- Tạo report sections.
- Tạo manual precision summary cho retrieval.

File quan trọng:

```text
results/module5/final_metrics_summary.csv
results/module5/manual_precision_overall.csv
results/module5/final_project_summary.json
results/module5/error_analysis.md
```

Nói đơn giản:

> Module 5 là phần tổng hợp và đánh giá cuối cùng để đưa vào báo cáo.

---

## 12. Module 6: Aspect-aware Hybrid Retrieval

File chính:

```text
src/module6_query_intent.py
src/module6_aspect_sentiment.py
src/module6_hybrid_retrieval.py
src/module6_reranker.py
scripts/run_module6_hybrid_rerank_demo.py
scripts/evaluate_module6_retrieval.py
```

Module 6 sinh ra để cải thiện điểm yếu của dense retrieval.

### 12.1. Vì sao cần Module 6?

Dense retrieval mạnh khi câu hỏi và review khác từ nhưng cùng nghĩa. Nhưng có thể bỏ sót các keyword ngắn như:

- sai size,
- móp hộp,
- thiếu phụ kiện,
- shop không rep,
- giao sai hàng,
- hàng bị lỗi.

BM25 lại mạnh khi query và review có từ khóa giống nhau.

Vì vậy Module 6 kết hợp:

```text
BM25 keyword search
+ Dense FAISS retrieval
+ RRF fusion
+ aspect rules
+ optional reranker
```

### 12.2. BM25 là gì?

BM25 là thuật toán tìm kiếm theo keyword.

Ví dụ query có từ `đóng gói`, review cũng có `đóng gói`, `hộp`, `seal`, thì BM25 dễ kéo review đó lên.

### 12.3. Dense retrieval là gì?

Dense retrieval dùng embedding để tìm theo ý nghĩa.

Ví dụ:

```text
giao hàng chậm
ship lâu
vận chuyển trễ
```

Dù từ khác nhau, embedding có thể xem là gần nghĩa.

### 12.4. RRF là gì?

RRF = Reciprocal Rank Fusion.

Nó gộp ranking từ BM25 và Dense. Nếu một review xuất hiện cao ở cả hai ranking, nó được ưu tiên hơn.

### 12.5. Aspect-aware rules là gì?

Aspect là khía cạnh/phương diện của review.

Ví dụ:

| Aspect | Từ khóa |
|---|---|
| giao_hang | giao hàng, ship, vận chuyển, giao chậm |
| chat_luong | lỗi, hỏng, kém, không dùng được |
| dong_goi | đóng gói, hộp, seal, bể, vỡ |
| dich_vu_shop | shop, tư vấn, hỗ trợ, rep |
| mau_ma_size_mau | size, rộng, chật, sai màu, không đúng mẫu |
| gia | giá, rẻ, đắt, đáng tiền |

Module 6 dùng aspect để rerank hoặc lọc tốt hơn.

### 12.6. Kết quả benchmark Module 6

Benchmark nhỏ, handcrafted/proxy:

| Mode | keyword_hit@5 | keyword_hit@10 | aspect_hit@5 | aspect_hit@10 |
|---|---:|---:|---:|---:|
| BM25 | 0,500 | 0,667 | 1,000 | 1,000 |
| Dense | 0,500 | 0,833 | 1,000 | 1,000 |
| Hybrid | 1,000 | 1,000 | 1,000 | 1,000 |
| Hybrid + reranker | 1,000 | 1,000 | 1,000 | 1,000 |

Cách nói đúng:

> Module 6 cho thấy hybrid retrieval có tiềm năng cải thiện khả năng bắt keyword/aspect trong benchmark nhỏ. Tuy nhiên đây chưa phải đánh giá lớn thay thế hoàn toàn manual Precision@k.

Không nói quá:

> Không nói Module 6 đã chứng minh hệ thống hoàn hảo. Chỉ nói đây là hướng nâng cấp có kết quả proxy tốt.

---

## 13. Sentiment model và RAG liên kết với nhau như thế nào?

Đây là câu hỏi rất dễ bị hỏi.

Trả lời ngắn:

> Sentiment model phân loại cảm xúc review. Kết quả sentiment sau đó được dùng trong phân tích dữ liệu và làm metadata/filter cho RAG, ví dụ khi người dùng hỏi về phàn nàn thì hệ thống ưu tiên review tiêu cực.

Chi tiết:

1. Module 2 tạo model sentiment.
2. Review/corpus có trường sentiment hoặc predicted_sentiment.
3. RAG retrieval có thể filter theo sentiment:
   - Hỏi phàn nàn -> ưu tiên negative.
   - Hỏi điểm tốt -> ưu tiên positive.
   - Hỏi chung -> có thể lấy tất cả.
4. Web app tách riêng:
   - Tab Sentiment: phân tích một review cụ thể.
   - Tab RAG: hỏi đáp trên kho review.
5. Tab kỹ thuật giải thích sentiment được dùng như metadata/filter trong RAG.

Điểm cần nhấn:

> Sentiment và RAG không phải hai phần rời rạc hoàn toàn. Sentiment giúp RAG chọn evidence đúng chiều cảm xúc hơn.

---

## 14. Web app demo

File chính:

```text
backend/app.py
frontend/index.html
frontend/styles.css
frontend/app.js
scripts/run_rag_webapp.py
```

Cách chạy:

```powershell
cd "C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted"
python scripts\run_rag_webapp.py
```

Mở:

```text
http://127.0.0.1:8000
```

Lưu ý:

- Phải có port `:8000`.
- Nếu mở `http://127.0.0.1` không có port thì có thể lỗi connection refused.

### 14.1. Tab 1: Phân tích Sentiment

Dùng để nhập một review thật.

Ví dụ:

```text
Shop giao sai màu, nhắn tin hỗ trợ nhưng không trả lời.
```

Output:

- Sentiment dự đoán.
- Model đang dùng.
- Giải thích ngắn.

Điểm cần nói:

> Tab này demo Module 2, tức model sentiment classification.

### 14.2. Tab 2: Hỏi đáp RAG

Dùng để hỏi trên kho review.

Ví dụ:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
Có review nào nói hàng bị lỗi hoặc hỏng không?
Khách hàng chê chất lượng sản phẩm ở điểm nào?
```

Output:

- Hệ thống hiểu câu hỏi.
- Câu trả lời có bằng chứng.
- Review được truy xuất.
- Chi tiết kỹ thuật.

Điểm cần nói:

> Tab này demo Module 4 và một phần logic nâng cấp retrieval/filter. Câu trả lời dựa trên evidence thật, không tự bịa.

### 14.3. Tab 3: Kỹ thuật & đánh giá

Hiển thị:

- Kho review: 82.677 documents.
- Embedding model: multilingual-E5-small.
- Retrieval method.
- Baseline Precision@5.
- Đường dẫn artifact.

Điểm cần nói:

> Tab này giúp người xem biết hệ thống đang dùng model/index nào và metric hiện tại ra sao.

---

## 15. Kịch bản thuyết trình 5 phút

### Phút 0:00 - 0:40: Giới thiệu bài toán

Nói:

> Đề tài của nhóm là ứng dụng NLP và RAG để phân tích cảm xúc review sản phẩm TMĐT. Vấn đề là review rất nhiều, nếu đọc thủ công sẽ khó nắm khách hàng đang khen/chê gì. Vì vậy nhóm xây dựng hệ thống gồm model phân loại sentiment và RAG để hỏi đáp có bằng chứng từ review thật.

### Phút 0:40 - 1:30: Nói về dữ liệu

Nói:

> Phần sentiment có 5.162 review sau dedup, chia thành negative, neutral, positive dựa trên rating. Phần RAG final dùng 82.677 documents, được build thành FAISS index bằng embedding model intfloat/multilingual-e5-small.

Nếu cần show code/file:

```text
data/reports/data_summary.json
models/module4/module4_index_config.json
```

### Phút 1:30 - 2:20: Nói về sentiment model

Nói:

> Nhóm thử majority baseline, TF-IDF + Logistic Regression và TF-IDF + Linear SVM. Model tốt nhất là Linear SVM với test accuracy 0,9329 và macro-F1 0,9098. Neutral là lớp khó nhất vì ít dữ liệu hơn và review 3 sao thường lẫn cả khen lẫn chê.

Show code:

```text
src/module2_baseline_sentiment_classification.py
results/module2/metrics_summary.csv
models/module2/best_model.joblib
```

### Phút 2:20 - 3:20: Nói về RAG

Nói:

> Với RAG, hệ thống encode review thành embedding, lưu trong FAISS index. Khi người dùng hỏi, query cũng được encode, sau đó tìm top-k review liên quan. Câu trả lời được tạo theo template có citation, không gọi LLM bên ngoài, nên câu trả lời chỉ dựa trên evidence truy xuất.

Show code:

```text
src/module4_retrieve.py
src/module4_rag_pipeline.py
models/module4/review_faiss.index
models/module4/review_metadata.parquet
```

### Phút 3:20 - 4:20: Demo web

Thứ tự demo:

1. Mở tab Sentiment.
2. Nhập review:

```text
Shop giao sai màu, nhắn tin hỗ trợ nhưng không trả lời.
```

3. Mở tab RAG.
4. Hỏi:

```text
Khách hàng phàn nàn gì về giao hàng chậm?
```

5. Chỉ vào citation và evidence cards.
6. Mở tab Kỹ thuật & đánh giá, chỉ số 82.677 documents và Precision@5.

### Phút 4:20 - 5:00: Kết luận

Nói:

> Hệ thống đã hoàn thành pipeline end-to-end: xử lý dữ liệu, huấn luyện sentiment model, phân tích review, xây dựng RAG có evidence và giao diện demo. Điểm mạnh là có thể vừa dự đoán cảm xúc từng review, vừa trả lời câu hỏi tổng hợp dựa trên review thật. Hạn chế là sentiment label lấy từ rating có thể nhiễu và RAG hiện là template-based, chưa phải LLM tự do.

---

## 16. Khi show code nên mở file nào?

### Nếu muốn show pipeline dữ liệu

```text
src/module1_data_layer.py
```

Nói:

> Đây là phần làm sạch, dedup, mapping rating sang sentiment và chia train/valid/test.

### Nếu muốn show model sentiment

```text
src/module2_baseline_sentiment_classification.py
```

Nói:

> Đây là phần train TF-IDF + Logistic Regression và TF-IDF + Linear SVM, sau đó chọn best model theo validation macro-F1.

### Nếu muốn show RAG retrieval

```text
src/module4_retrieve.py
```

Nói:

> Đây là phần load FAISS index và metadata, encode query bằng multilingual-E5, rồi retrieve top-k review.

### Nếu muốn show RAG answer

```text
src/module4_rag_pipeline.py
src/module4_rag_pipeline_upgraded.py
```

Nói:

> Đây là phần build evidence và tạo answer có citation theo template.

### Nếu muốn show Module 6

```text
src/module6_hybrid_retrieval.py
src/module6_query_intent.py
src/module6_reranker.py
```

Nói:

> Đây là hướng nâng cấp retrieval bằng BM25 + Dense + RRF/rerank và aspect rules.

### Nếu muốn show web app

```text
backend/app.py
frontend/app.js
frontend/index.html
frontend/styles.css
```

Nói:

> Backend cung cấp API, frontend gọi API và render kết quả thành các tab.

---

## 17. Câu hỏi có thể bị hỏi và cách trả lời

### Q1. Project của bạn dùng phương pháp nào?

Trả lời:

> Project dùng TF-IDF + Linear SVM cho sentiment classification và multilingual-E5 + FAISS cho retrieval/RAG. Ngoài ra có Module 6 thử nghiệm hybrid retrieval gồm BM25, Dense FAISS, RRF/rerank và aspect-aware rules.

### Q2. Vì sao dùng TF-IDF + SVM mà không dùng BERT/PhoBERT?

Trả lời:

> TF-IDF + Linear SVM là baseline cổ điển nhưng rất mạnh cho text classification khi dữ liệu vừa phải. Với 5.162 review sentiment, Linear SVM đạt macro-F1 0,9098, nên đủ tốt cho phạm vi đề tài. PhoBERT/XLM-R có thể là hướng phát triển sau, nhưng cần nhiều tài nguyên hơn và cần fine-tune cẩn thận.

### Q3. TF-IDF hoạt động ra sao?

Trả lời:

> TF-IDF biến text thành vector dựa trên độ quan trọng của từ. Một từ càng xuất hiện nhiều trong review nhưng không quá phổ biến trong toàn corpus thì trọng số càng cao. Ví dụ `lỗi`, `hỏng`, `giao chậm` là tín hiệu mạnh cho review tiêu cực.

### Q4. Linear SVM hoạt động ra sao?

Trả lời:

> Linear SVM tìm một siêu phẳng để phân tách các lớp sentiment trong không gian vector TF-IDF. Nó phù hợp vì dữ liệu text sau TF-IDF có rất nhiều chiều và thưa.

### Q5. Vì sao chọn Linear SVM là model tốt nhất?

Trả lời:

> Vì Linear SVM có validation macro-F1 tốt nhất và trên test đạt accuracy 0,9329, macro-F1 0,9098, cao hơn Logistic Regression và majority baseline.

### Q6. Vì sao neutral yếu hơn?

Trả lời:

> Neutral chỉ có 871 mẫu, ít hơn positive và negative. Ngoài ra review 3 sao thường có cả khen lẫn chê, nên bản chất nó mơ hồ hơn. Vì vậy F1 của neutral là 0,8230, thấp hơn negative và positive.

### Q7. Label sentiment lấy từ đâu?

Trả lời:

> Label sentiment được ánh xạ từ rating: 1-2 sao là negative, 3 sao là neutral, 4-5 sao là positive. Đây là cách phổ biến khi chưa có nhãn thủ công, nhưng có thể nhiễu vì rating không phải lúc nào cũng khớp nội dung review.

### Q8. RAG là gì?

Trả lời:

> RAG là Retrieve-Augment-Generate. Trong project này, hệ thống retrieve review liên quan từ FAISS index, sau đó generate câu trả lời dựa trên evidence đã retrieve. Câu trả lời có citation để người dùng kiểm chứng.

### Q9. RAG của bạn có dùng ChatGPT hay LLM không?

Trả lời:

> Không. RAG trong project là evidence-grounded/template-based answer generation. Hệ thống không gọi API LLM bên ngoài. Cách này giúp kiểm soát tốt hơn, tránh bịa nội dung ngoài review.

### Q10. FAISS dùng để làm gì?

Trả lời:

> FAISS dùng để lưu và tìm kiếm embedding của review. Khi có query, hệ thống encode query thành vector rồi FAISS tìm các review có vector gần nhất.

### Q11. Embedding model là gì?

Trả lời:

> Project dùng intfloat/multilingual-e5-small. Đây là model embedding đa ngôn ngữ, biến query và review thành vector 384 chiều để tìm kiếm theo ngữ nghĩa.

### Q12. Vì sao dùng prefix `query:` và `passage:`?

Trả lời:

> multilingual-E5 được huấn luyện theo format query/passage, nên khi encode query dùng `query:` và khi encode review dùng `passage:` để đúng cách model học.

### Q13. Precision@5 0,5067 nghĩa là gì?

Trả lời:

> Trên bộ 15 query được chấm tay, trung bình trong 5 review hệ thống trả về có khoảng 50,67% review liên quan. Đây là baseline retrieval, cho thấy hệ thống có bằng chứng liên quan nhưng vẫn còn dư địa cải thiện.

### Q14. Tại sao Precision@5 không cao hơn?

Trả lời:

> Vì query tiếng Việt có nhiều cách diễn đạt, review có nhiễu, có lỗi chính tả, có review cùng chủ đề nhưng sai intent hoặc sai sentiment. Dense retrieval có thể lấy review gần nghĩa nhưng không đúng khía cạnh cụ thể. Vì vậy nhóm thêm Module 6 để cải thiện bằng BM25 và aspect rules.

### Q15. Module 6 là gì?

Trả lời:

> Module 6 là hướng nâng cấp retrieval. Nó kết hợp BM25 keyword search, Dense FAISS retrieval, RRF fusion, optional reranker và aspect-aware rules để bắt tốt hơn các vấn đề như giao hàng, đóng gói, sai hàng, thiếu hàng, chất lượng, size.

### Q16. Module 6 có phải ABSA hoàn chỉnh không?

Trả lời:

> Không. Module 6 mới là MVP/experimental enhancement dạng rule-based và hybrid retrieval. Nó có aspect rules nhưng chưa phải supervised ABSA model được huấn luyện riêng.

### Q17. Sentiment và RAG liên quan gì?

Trả lời:

> Sentiment model giúp gán/khai thác cảm xúc của review. Trong RAG, sentiment được dùng như metadata/filter. Ví dụ khi hỏi "phàn nàn", hệ thống ưu tiên review negative để evidence đúng hướng hơn.

### Q18. Nếu query hỏi về giao hàng thì hệ thống hiểu bằng cách nào?

Trả lời:

> Hệ thống có intent/aspect detection rule-based. Nếu query có từ như `giao hàng`, `ship`, `vận chuyển`, `giao chậm`, thì nó nhận diện aspect giao_hang, mở rộng query bằng các từ liên quan và ưu tiên sentiment negative nếu có dấu hiệu phàn nàn.

### Q19. Query expansion là gì?

Trả lời:

> Query expansion là mở rộng câu hỏi bằng từ đồng nghĩa hoặc từ liên quan. Ví dụ `giao hàng chậm` có thể mở rộng thành `ship trễ`, `giao lâu`, `vận chuyển lâu`. Điều này giúp retrieval tìm được review dù người dùng và khách hàng dùng từ khác nhau.

### Q20. Hệ thống có thể bịa câu trả lời không?

Trả lời:

> Thiết kế hiện tại hạn chế bịa vì answer generator chỉ dựa trên review được retrieve và có citation. Nếu evidence yếu, hệ thống phải nói chưa đủ bằng chứng rõ ràng.

### Q21. Điểm mạnh của project là gì?

Trả lời:

> Project có pipeline end-to-end: xử lý dữ liệu, train sentiment, phân tích review, build RAG index, đánh giá retrieval và web demo. Kết quả sentiment khá tốt với macro-F1 0,9098, và RAG có evidence/citation giúp kiểm chứng.

### Q22. Hạn chế lớn nhất là gì?

Trả lời:

> Label sentiment lấy từ rating nên có thể nhiễu. Retrieval Precision@5 còn ở mức baseline 0,5067. RAG chưa dùng LLM thật nên câu trả lời an toàn nhưng chưa linh hoạt như chatbot hoàn chỉnh. Module 6 mới là benchmark nhỏ.

### Q23. Nếu phát triển tiếp thì làm gì?

Trả lời:

> Có thể fine-tune PhoBERT/XLM-R cho sentiment, xây dựng dataset ABSA tiếng Việt, huấn luyện reranker supervised, mở rộng manual relevance evaluation, và tích hợp LLM có kiểm soát citation để câu trả lời tự nhiên hơn nhưng vẫn không bịa.

### Q24. Dữ liệu 82.677 có được update thật chưa?

Trả lời:

> Có. File final `data/processed/rag_corpus_module4.csv`, `models/module4/review_metadata.parquet` và `models/module4/module4_index_config.json` đều xác nhận 82.677 documents. Các summary cũng đã được sync lại theo artifact final.

### Q25. Nếu người xem hỏi "show code phần chạy RAG ở đâu?"

Trả lời:

> Em sẽ mở `src/module4_retrieve.py` để show phần load FAISS, encode query và retrieve review; sau đó mở `src/module4_rag_pipeline.py` để show phần build evidence và tạo answer có citation.

---

## 18. Những câu nên nói thật để tránh bị bắt bẻ

Không nên nói:

```text
Hệ thống RAG dùng LLM thông minh để tự sinh câu trả lời.
```

Nên nói:

```text
Hệ thống dùng template-based generation dựa trên evidence được truy xuất, chưa gọi LLM bên ngoài.
```

Không nên nói:

```text
Module 6 chứng minh retrieval hoàn hảo.
```

Nên nói:

```text
Module 6 cho thấy hybrid retrieval cải thiện keyword/aspect hit-rate trong benchmark nhỏ, nhưng cần đánh giá lớn hơn để kết luận chắc chắn.
```

Không nên nói:

```text
Sentiment label hoàn toàn đúng.
```

Nên nói:

```text
Sentiment label được suy ra từ rating, vì vậy có thể có nhiễu. Đây là một hạn chế của đề tài.
```

Không nên nói:

```text
Precision@5 thấp nhưng không quan trọng.
```

Nên nói:

```text
Precision@5 là baseline retrieval hiện tại. Nó cho thấy hệ thống đã lấy được evidence liên quan ở mức nhất định, nhưng vẫn còn dư địa cải thiện bằng hybrid retrieval và reranking.
```

---

## 19. Lệnh chạy cần nhớ

### Chạy web app

```powershell
cd "C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted"
python scripts\run_rag_webapp.py
```

Mở:

```text
http://127.0.0.1:8000
```

### Test API health

```text
http://127.0.0.1:8000/api/health
```

### Chạy Module 6 demo

```powershell
python scripts\run_module6_hybrid_rerank_demo.py --query "Khach phan nan gi ve giao hang cham?" --top-candidates 50 --top-evidence 5 --use-reranker false --target-aspect giao_hang
```

### Nếu server báo port 8000 đang bận

Nguyên nhân:

> Có server cũ đang chạy.

Cách xử lý:

- Tắt terminal đang chạy server bằng `CTRL + C`.
- Hoặc chạy lại sau khi đóng tiến trình cũ.

---

## 20. File quan trọng cần nhớ

### Data

```text
data/reports/data_summary.json
data/processed/sentiment_reviews.csv
data/processed/rag_corpus_module4.csv
```

### Model sentiment

```text
models/module2/best_model.joblib
models/module2/tfidf_linearsvm.joblib
models/module2/tfidf_logreg.joblib
models/module2/label_mapping.json
```

### RAG artifacts

```text
models/module4/review_faiss.index
models/module4/review_metadata.parquet
models/module4/module4_index_config.json
```

### Metrics

```text
results/module2/metrics_summary.csv
results/module5/manual_precision_overall.csv
results/module5/final_project_summary.json
results/module6/last_benchmark_console_reference.txt
```

### Backend/frontend

```text
backend/app.py
frontend/index.html
frontend/styles.css
frontend/app.js
```

### Báo cáo

```text
report_latex/main.tex
report_latex/chapters/
```

---

## 21. Checklist trước khi thuyết trình

Trước khi vào buổi thuyết trình:

- Mở được web app ở `http://127.0.0.1:8000`.
- Test tab Sentiment với một review tiêu cực.
- Test tab RAG với câu hỏi giao hàng chậm.
- Mở sẵn `data_summary.json` để chứng minh 82.677 documents.
- Mở sẵn `metrics_summary.csv` để chứng minh Linear SVM tốt nhất.
- Mở sẵn `module4_index_config.json` để chứng minh embedding model/FAISS config.
- Mở sẵn `src/module4_retrieve.py` để show code RAG.
- Mở sẵn `src/module2_baseline_sentiment_classification.py` để show code sentiment.
- Chuẩn bị câu trả lời về:
  - Vì sao dùng SVM.
  - Vì sao neutral yếu.
  - RAG có dùng LLM không.
  - Precision@5 nghĩa là gì.
  - Data đã update từ 45k lên 82.677 chưa.

---

## 22. Một đoạn kết luận có thể học thuộc

> Tóm lại, đề tài đã xây dựng được một pipeline NLP end-to-end cho review TMĐT tiếng Việt. Phần sentiment classification dùng TF-IDF + Linear SVM và đạt macro-F1 0,9098 trên test set. Phần RAG dùng multilingual-E5 và FAISS để truy xuất review liên quan từ kho 82.677 documents, sau đó tạo câu trả lời có citation dựa trên evidence. Web demo tách rõ phân tích sentiment, hỏi đáp RAG và thông tin kỹ thuật. Hạn chế hiện tại là nhãn sentiment được suy ra từ rating, retrieval Precision@5 còn ở mức baseline và RAG chưa dùng LLM thật. Hướng phát triển là fine-tune mô hình ngôn ngữ tiếng Việt, huấn luyện reranker và mở rộng đánh giá relevance.

