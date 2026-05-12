# CHECKLIST CH?M ?I?M

| Ti?u ch? | ?? ??p ?ng | V? tr? trong b?o c?o | Ghi ch? |
|---|---:|---|---|
| Trang b?a c? placeholder d? s?a | C? | main.tex | D?ng bi?n LaTeX cho sinh vi?n, MSSV, tr??ng, khoa, gi?ng vi?n, th?i gian. |
| Front matter d?ng s? La M? | C? | main.tex | Ch??ng 1 chuy?n v? s? ? R?p. |
| N?u ??ng RAG kh?ng d?ng LLM th?t | C? | T?m t?t, Ch??ng 5, 8, 10, Ph? l?c | Evidence-grounded/template-based generation. |
| S? li?u sentiment ??ng | C? | Ch??ng 4, 6 | 5.162 review sau dedup; positive 2.217, negative 2.074, neutral 871. |
| K?t qu? model sentiment ??ng | C? | Ch??ng 6 | Linear SVM accuracy 0,9329; macro-F1 0,9098; weighted-F1 0,9315. |
| Confusion matrix d?ng s? | C? | Ch??ng 6 | Negative ??ng 304/311, neutral ??ng 100/131, positive ??ng 319/333. |
| RAG final 82.677 documents | C? | Ch??ng 4, 8, 11, Ph? l?c | ?u ti?n module4_index_config.json v? review_metadata.parquet. |
| Gi?i th?ch 45.259 vs 82.677 | C? | Ch??ng 4, Ph? l?c | 45.259 l? summary/artifact c?. |
| H?nh category RAG final | C? | Ch??ng 4 | Regenerate t? models/module4/review_metadata.parquet. |
| Precision@k retrieval | C? | Ch??ng 6, Ph? l?c | P@3=0,4222; P@5=0,5067; P@10=0,4867. |
| Module 6 benchmark | C? | Ch??ng 6, Ph? l?c | Ghi r? benchmark nh?/handcrafted, ch? l? proxy. |
| S? ?? ki?n tr?c | C? | Ch??ng 3 | D?ng TikZ pipeline. |
| API backend v? demo web | C? | Ch??ng 8, Ph? l?c | C? endpoint, input/output, v? d? JSON. |
| Ph? l?c kh?ng b? l?p ti?u ?? | C? | chapters/appendix.tex | Chuy?n th?nh nhi?u chapter ph? l?c r? r?ng. |
| T?i li?u tham kh?o m? r?ng | C? | references.bib, Ch??ng 2 | 20 ngu?n th?t v? ??u ???c cite. |
| Bi?n d?ch local | Ch?a x?c nh?n | report_latex/ | M?i tr??ng hi?n kh?ng c? xelatex/latexmk; c?n compile tr?n Overleaf ho?c MiKTeX/TeX Live. |
