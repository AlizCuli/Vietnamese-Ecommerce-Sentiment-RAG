#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
else
  xelatex -interaction=nonstopmode -file-line-error main.tex
  bibtex main || true
  xelatex -interaction=nonstopmode -file-line-error main.tex
  xelatex -interaction=nonstopmode -file-line-error main.tex
fi
if [ -f main.pdf ]; then
  cp main.pdf TIEU_LUAN_NLP_RAG_FINAL.pdf
fi
