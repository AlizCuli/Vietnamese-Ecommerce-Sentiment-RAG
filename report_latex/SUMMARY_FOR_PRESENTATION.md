# SUMMARY FOR PRESENTATION

## B?i to?n
?? t?i x?y d?ng h? th?ng ph?n t?ch review TM?T ti?ng Vi?t b?ng NLP v? Retrieval-Augmented Generation. H? th?ng c? hai ch?c n?ng ch?nh: ph?n lo?i c?m x?c t?ng review v? h?i ??p RAG d?a tr?n review th?t c? citation.

## D? li?u
D? li?u sentiment sau x? l? c? 5.162 review: positive 2.217, negative 2.074, neutral 871. Nh?n sentiment ???c ?nh x? t? rating: 1-2 sao l? negative, 3 sao l? neutral, 4-5 sao l? positive. RAG final d?ng 82.677 documents theo models/module4/module4_index_config.json v? models/module4/review_metadata.parquet.

## Ph??ng ph?p
Module 1 l?m s?ch d? li?u, x? l? duplicate v? t?o split. Module 2 hu?n luy?n majority baseline, TF-IDF + Logistic Regression v? TF-IDF + Linear SVM. Module 3 t?o analytics. Module 4 d?ng multilingual-E5-small + FAISS IndexFlatIP ?? truy xu?t review v? t?o answer template c? citation. Module 5 t?ng h?p evaluation/error analysis. Module 6 th? hybrid retrieval b?ng BM25 + Dense FAISS + RRF/rerank + aspect-aware rules.

## K?t qu? ch?nh
Linear SVM l? model sentiment t?t nh?t: test accuracy 0,9329, macro-F1 0,9098, weighted-F1 0,9315. L?p neutral l? ?i?m y?u ch?nh: F1 0,8230, ??ng 100/131 v? 23 m?u b? nh?m sang negative. Retrieval baseline c? Manual Precision@5 = 0,5067 tr?n 15 query. Module 6 hybrid ??t keyword_hit@5 = 1,000 trong benchmark nh?, nh?ng ??y ch? l? proxy, ch?a thay th? evaluation l?n.

## Demo
Ch?y web b?ng: `python scripts\run_rag_webapp.py`, m? `http://127.0.0.1:8000`. Demo theo th? t?: tab Ph?n t?ch Sentiment, tab H?i ??p RAG, evidence/citation, tab K? thu?t & ??nh gi?. Nh?n m?nh h? th?ng kh?ng c?n API key v? kh?ng g?i LLM b?n ngo?i.

## H?n ch? v? h??ng ph?t tri?n
Nh?n sentiment l?y t? rating n?n c? nhi?u. Neutral ?t d? li?u v? d? l?n. TF-IDF + SVM ch?a hi?u ng? c?nh s?u nh? PhoBERT/XLM-R. Retrieval precision c?n ? m?c baseline. RAG hi?n l? template-based. H??ng ph?t tri?n g?m fine-tune PhoBERT/XLM-R, x?y dataset ABSA ti?ng Vi?t, supervised reranker, m? r?ng human evaluation v? t?ch h?p LLM c? ki?m so?t citation.
