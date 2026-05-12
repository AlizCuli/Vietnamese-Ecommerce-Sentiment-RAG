# FINAL_POLISH_REPORT

## 1. Các lỗi trình bày đã sửa

- Cập nhật `main.tex` để dùng macro path an toàn hơn: `\code`, `\codepath`, `\filepath` đều dựa trên `\path{...}` nhằm hạn chế tràn lề với tên file, endpoint, model name và đường dẫn dài.
- Bổ sung/cấu hình các package hỗ trợ trình bày: `microtype`, `xurl`, `url`, `seqsplit`, `tabularx`, `longtable`, `ragged2e`, `listings`.
- Tăng khả năng xử lý dòng dài bằng `\emergencystretch=4em`, `\tolerance=2000`, `\hbadness=10000`.
- Sửa các bảng path dài ở Chương 4, Chương 8 và phụ lục bằng `tabularx`, `longtable`, cột `L{...}` và `\filepath{...}`.
- Thiết kế lại phụ lục để không còn bảng artifact bị chồng chữ/tràn cột.

## 2. Nội dung không phù hợp với tiểu luận đã xóa hoặc viết lại

- Xóa nội dung mang tính luyện thuyết trình, vấn đáp, hướng dẫn trình bày ngắn và ghi chú cá nhân.
- Viết lại Chương 8 sang “Triển khai thử nghiệm và giao diện hệ thống”.
- Viết lại các mục trong Chương 6:
  - “Cách giải thích Precision@5 trước hội đồng” thành “Diễn giải chỉ số Precision@k”.
  - “Cách giải thích Module 6 trước hội đồng” thành “Diễn giải kết quả benchmark Module 6”.
- Thiết kế lại phụ lục theo hướng học thuật:
  - Cấu trúc thư mục và artifact.
  - Hướng dẫn tái lập thực nghiệm.
  - API backend.
  - Ví dụ input/output.
  - Pseudocode pipeline.
  - Bảng metric bổ sung.
  - Ghi chú đạo đức và trách nhiệm.
- Xóa các file ghi chú review cũ có nội dung không còn phù hợp:
  - `FINAL_REVIEW.md`
  - `REVIEW_FIXES_APPLIED.md`

## 3. Văn phong đã chuẩn hóa

- Giảm dùng từ “project” trong phần báo cáo chính; ưu tiên “đề tài”, “hệ thống”, “mã nguồn thực nghiệm”, “pipeline”.
- Thay các câu dạng hướng dẫn trình bày bằng câu học thuật, ví dụ:
  - “Kết quả này cho thấy...”
  - “Chỉ số này được diễn giải như sau...”
  - “Trong phạm vi đánh giá của đề tài...”
  - “Một hạn chế của phương pháp là...”
- Không mô tả hệ thống như sản phẩm production; báo cáo vẫn ghi rõ đây là hệ thống thử nghiệm học thuật.
- Nhấn mạnh RAG là evidence-grounded/template-based answer generation, không gọi API LLM bên ngoài.

## 4. Hình RAG category

- Báo cáo không dùng hình category cũ có nguy cơ phản ánh corpus 45.259 documents.
- Báo cáo dùng hình final:
  - `report_latex/figures_generated/rag_category_distribution_final.png`
- Caption ghi rõ hình tương ứng với RAG corpus final 82.677 documents.
- Chương 4 cũng giải thích khác biệt giữa summary cũ 45.259 documents và cấu hình final 82.677 documents theo `models/module4/module4_index_config.json`.

## 5. Tài liệu tham khảo

- `references.bib` đã được mở rộng lên 23 nguồn.
- Bổ sung các nguồn cho Dense Passage Retrieval, ABSA và FastAPI:
  - `karpukhin2020dense`
  - `pontiki2014semeval`
  - `fastapi`
- Kiểm tra tĩnh cho thấy không có bib key bị thiếu hoặc chưa được cite.

## 6. Kiểm tra tĩnh đã thực hiện

- Không còn các cụm không phù hợp với văn phong tiểu luận trong các file `.tex` và `.md`.
- Không phát hiện missing reference trong kiểm tra tĩnh.
- Không phát hiện bib key thiếu hoặc unused trong kiểm tra tĩnh.
- Các số liệu chính vẫn giữ đúng:
  - Sentiment sau dedup: 5.162 review.
  - Linear SVM test accuracy: 0,9329.
  - Linear SVM test macro-F1: 0,9098.
  - RAG final documents: 82.677.
  - Embedding model: `intfloat/multilingual-e5-small`.
  - FAISS: `IndexFlatIP`, dim 384.
  - Manual Precision@5: 0,5067.
  - Module 6 hybrid keyword_hit@5: 1,000 trong benchmark nhỏ.

## 7. Biên dịch PDF

- Đã chạy `compile.ps1`, nhưng máy hiện tại chưa cài hoặc chưa nhận `xelatex` và `bibtex` trong PATH.
- Lỗi môi trường:
  - `xelatex : The term 'xelatex' is not recognized`
  - `bibtex : The term 'bibtex' is not recognized`
- Vì vậy chưa thể tạo `TIEU_LUAN_NLP_RAG_FINAL.pdf` trong máy local này.
- Số trang PDF final: chưa xác định do thiếu TeX compiler local.

## 8. Việc cần người dùng tự điền

- Trong `main.tex`, các biến trang bìa còn cần sửa trước khi nộp:
  - `\studentName{Họ tên sinh viên}`
  - `\studentId{MSSV}`
  - `\universityName{Tên trường}`
  - `\facultyName{Tên khoa/bộ môn}`
  - `\instructorName{Tên giảng viên}`
  - `\reportDate{Tháng/Năm}`

## 9. Cách biên dịch khuyến nghị

Nếu dùng Overleaf:

1. Upload toàn bộ thư mục `report_latex/`.
2. Đảm bảo các thư mục `figures/` nếu cần hình từ project root cũng được upload đúng vị trí tương đối.
3. Menu `Settings` chọn compiler `XeLaTeX`.
4. File chính chọn `main.tex`.
5. Bấm `Recompile`.

Nếu dùng local sau khi cài MiKTeX/TeX Live:

```powershell
cd "C:\Users\PC\PycharmProjects\PythonProject\ML\PROJECT\Sàn TMDT\Chí Bình\ecommerce_sentiment_rag_final_submission_extracted\report_latex"
powershell -ExecutionPolicy Bypass -File .\compile.ps1
```

## 10. Hạn chế còn lại

- Chưa kiểm tra trực quan PDF vì môi trường local không có `xelatex`/`bibtex`.
- Chưa xác nhận số trang thực tế sau biên dịch.
- Nếu Overleaf báo overfull hbox nhỏ, ưu tiên kiểm tra các bảng dài ở phụ lục và các caption chứa path; các macro path đã được chuẩn bị để giảm rủi ro này.
