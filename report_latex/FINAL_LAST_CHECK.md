# FINAL LAST CHECK

## Các lỗi đã sửa

- Giữ bố cục trang bìa theo mẫu chốt: tên trường, khoa, tiêu đề tiểu luận, tên đề tài, danh sách sinh viên, giảng viên và thời gian.
- Xóa đoạn chú thích nội bộ khỏi trang bìa để bìa gọn và trang trọng hơn.
- Quét toàn bộ file `.tex`; không còn ký tự lỗi `￾`.
- Đảm bảo các cụm lỗi như `TF￾IDF`, `macro￾F1`, `evidence￾grounded`, `multilingual￾E5`, `rating￾sentiment`, `human-in￾the-loop` không còn xuất hiện.
- Đặt tên danh mục trong LaTeX là `Danh mục hình` và `Danh mục bảng`.
- Rút gọn bảng artifact chính ở Chương 5, chỉ hiển thị tên file ngắn trong bảng chính để tránh path dài bị ngắt dòng xấu.
- Tách dòng nguồn dưới Bảng 4.8 thành một dòng riêng: `Nguồn: models/module4/review_metadata.parquet`.
- Kiểm tra source không còn placeholder nội dung kiểu `nếu có ảnh`, `báo cáo sẽ tự động chèn`, `macro safeimage`, hoặc lỗi encoding tiếng Việt trong code block theo các mẫu đã phát hiện.
- Kiểm tra các ảnh chính được tham chiếu trong báo cáo đều tồn tại trong thư mục project.

## Số liệu chính được giữ nguyên

- Sentiment dataset sau xử lý duplicate: 5.162 review.
- Linear SVM test macro-F1: 0,9098.
- RAG corpus/index final: 82.677 documents.
- Manual Precision@5: 0,5067.

## Thông tin cần tự kiểm tra trước khi nộp

- MSSV của Phan Tấn Phúc đang được ghi là `2351060029`, trùng với Tạ Chí Bình. Nếu đây không phải mã thật, cần sửa trực tiếp trong `main.tex`.
- Thời gian trên bìa đang là `TP. Hồ Chí Minh, tháng 12 năm 2026`, theo thông tin người dùng cung cấp. Nếu giảng viên yêu cầu dùng tháng hiện tại hoặc học kỳ cụ thể, cần sửa trong `main.tex`.

## Biên dịch PDF

- Máy local hiện không có `xelatex` hoặc `latexmk`, nên chưa thể biên dịch và xác định số trang trực tiếp tại local.
- Bản zip Overleaf cuối cùng đã được chuẩn bị để biên dịch bằng XeLaTeX trên Overleaf.
- Khi upload lên Overleaf, chọn compiler `XeLaTeX`. Nếu Overleaf bị timeout, bấm compile lại hoặc tạm ẩn bớt ảnh, nhưng không bật draft mode khi xuất bản final.

## Tổng số trang PDF final

- Chưa xác định tại local do thiếu XeLaTeX/latexmk.
- Cần kiểm tra số trang sau khi biên dịch trên Overleaf.
