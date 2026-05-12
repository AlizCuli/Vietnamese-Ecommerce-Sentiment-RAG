# README MODULE 3 - Review Analytics

## Vai trò

Module 3 không huấn luyện model mới. Module này dùng dữ liệu sentiment đã có để tạo phân tích mô tả và biểu đồ cho báo cáo.

Nói đơn giản: **Module 3 biến kết quả sentiment thành bảng và biểu đồ dễ trình bày.**

## Input

```text
data/processed/sentiment_reviews.csv
data/processed/sentiment_reviews_5class.csv
data/reports/sentiment_label_distribution.csv
```

## Output chính

```text
results/module3/overall_sentiment_distribution.csv
results/module3/rating_sentiment_crosstab.csv
results/module3/top_negative_reviews.csv
results/module3/rag_sentiment_summary.json
figures/module3/
```

## Ý nghĩa output

- `overall_sentiment_distribution.csv`: phân phối Tiêu cực / Trung lập / Tích cực.
- `rating_sentiment_crosstab.csv`: quan hệ giữa rating và sentiment.
- `top_negative_reviews.csv`: các review tiêu cực tiêu biểu để phân tích lỗi.
- `figures/module3/`: biểu đồ dùng trong báo cáo và slide.

## Dùng trong báo cáo

Module 3 giúp trả lời:

- Dữ liệu có lệch sentiment không?
- Review tiêu cực thường có nội dung gì?
- Rating và sentiment có khớp nhau không?
- Dữ liệu có phù hợp cho bài toán phân tích cảm xúc không?

## Lưu ý

Module 3 là phần analytics, không ảnh hưởng trực tiếp đến model artifact hay FAISS index.
