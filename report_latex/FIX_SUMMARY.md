# FIX SUMMARY

Đã sửa các lỗi còn sót trong source LaTeX:

- Loại bỏ BOM/ký tự ẩn trong các file `.tex`.
- Thêm macro an toàn cho các thuật ngữ thường bị tách dòng xấu: TF-IDF, macro-F1, evidence-grounded, multilingual-E5, rating-sentiment.
- Kiểm tra bằng `pdftotext`: PDF sau khi build không còn ký tự lỗi `￾` hoặc ký tự thay thế `�`.
- Rút gọn các bảng có đường dẫn dài để giảm lỗi ngắt dòng xấu.
- Sửa Bảng 3.1, Bảng 4.1, Bảng 5.2 và Bảng A.2 để trình bày gọn hơn.
- Sửa dòng nguồn của Bảng 4.8 cho gọn và không chen vào bảng.
- Thêm fallback font `Liberation Serif` để có thể biên dịch trong môi trường thiếu Times New Roman/TeX Gyre Termes.
- Thêm định nghĩa `json` cho `listings` để compile ổn định khi dùng `language=json`.

Các thông tin trang bìa như MSSV và ngày tháng được giữ nguyên theo xác nhận của người dùng.
