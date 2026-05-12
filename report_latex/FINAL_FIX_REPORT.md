# FINAL FIX REPORT

## File đã sửa

- `report_latex/main.tex`
- `report_latex/chapters/appendix.tex`
- `report_latex/chapters/chapter04_data_preprocessing.tex`
- `report_latex/chapters/chapter05_methodology.tex`
- `report_latex/chapters/chapter06_experiments.tex`
- `report_latex/chapters/chapter08_web_demo.tex`
- `report_latex/references_static.tex`

## Sửa ảnh

- Kiểm tra `graphicx` không dùng chế độ `draft`.
- Thêm `\setkeys{Gin}{draft=false}` để hạn chế trường hợp Overleaf/draft mode chỉ hiển thị tên file ảnh.
- Sửa macro ảnh để nếu ảnh thiếu thì không in đường dẫn ảnh ra PDF.
- Gói Overleaf final chỉ đóng gói các ảnh thật sự được dùng trong báo cáo.
- Ảnh phân phối ngành hàng RAG dùng bản final `figures_generated/rag_category_distribution_final.png`, tương ứng corpus final 82.677 documents.

## Sửa lỗi tiếng Việt trong listing/code block

- Chuyển ví dụ JSON trong `chapter08_web_demo.tex` và `appendix.tex` sang tiếng Việt không dấu bên trong `lstlisting`.
- Thêm câu giải thích tiếng Việt có dấu ở ngoài code block để giữ nghĩa của ví dụ.
- Chuyển cấu trúc thư mục ở Phụ lục A từ `lstlisting` sang bảng `longtable`, tránh lỗi Unicode tiếng Việt trong verbatim/listing.

## Sửa front matter và trang bìa

- Chuẩn hóa tên trường: `Trường Đại học Mở Thành phố Hồ Chí Minh`.
- Chuẩn hóa tên khoa: `Khoa Khoa học Cơ bản`.
- Chuẩn hóa thời gian: `TP. Hồ Chí Minh, tháng 12 năm 2026`.
- Sửa lời cảm ơn từ văn phong cá nhân sang văn phong nhóm.
- Bổ sung ngắt trang trước khi chuyển sang đánh số Ả Rập để Chương 1 bắt đầu lại từ trang 1.
- Đảm bảo `Danh mục hình`, `Danh mục bảng`, `Danh mục từ viết tắt` thuộc front matter.

## Sửa nội dung meta không phù hợp

- Viết lại mục về trực quan hóa trong Chương 6, loại bỏ nội dung nói về macro LaTeX/safeimage/compile khi thiếu ảnh.
- Viết lại mục ảnh minh họa giao diện trong Chương 8 thành mô tả học thuật về giao diện thử nghiệm, không còn câu “Nếu có ảnh...” hoặc `IfFileExists`.
- Đổi tiêu đề `Tại sao báo cáo cần cả model và RAG` thành `Vai trò kết hợp giữa mô hình phân loại cảm xúc và tầng RAG`.

## Sửa caption và path dài

- Rút gọn caption có đường dẫn dài.
- Chuyển nguồn file dài xuống dòng ghi chú dưới bảng bằng `\filepath{...}`.
- Không đưa path dài vào caption chính để tránh vỡ danh mục hình/bảng.

## Kiểm tra tự động đã thực hiện

- Không còn các cụm: `Nếu có ảnh`, `báo cáo sẽ tự động`, `block dưới đây`, `Trong báo cáo LaTeX`, `LaTeX vẫn`, `macro safeimage`, `Tại sao báo cáo cần`, `quay video`, `thuyết minh 5 phút`, `thầy có thể hỏi`, `trước hội đồng`, `người không chuyên`.
- Không còn ký tự lỗi được yêu cầu kiểm tra như `TF￾`, `macro￾`, `evidence￾`, `rating￾`, `multilingual￾`.
- Không còn caption chứa path dài trực tiếp.
- Gói Overleaf final không chứa file rác `.aux`, `.log`, `.toc`, `.csv`, `.json`, `.md`, `.ps1`, `.sh`, `.bib`.

## Biên dịch PDF

- Máy local hiện không có `xelatex`, nên chưa thể biên dịch PDF trực tiếp trên máy này.
- Bản final đã được đóng gói để upload lên Overleaf và dùng compiler `XeLaTeX`.
- Tổng số trang PDF final cần kiểm tra lại trên Overleaf sau khi compile.

## Thông tin người dùng cần tự kiểm tra

- MSSV của Phan Tấn Phúc đang được giữ theo thông tin đã cung cấp (`2351060029`), trùng với Tạ Chí Bình. Cần xác nhận lại trước khi nộp chính thức.
