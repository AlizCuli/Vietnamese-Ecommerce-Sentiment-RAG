Set-Location $PSScriptRoot
if (Get-Command latexmk -ErrorAction SilentlyContinue) {
    latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
} else {
    xelatex -interaction=nonstopmode -file-line-error main.tex
    bibtex main
    xelatex -interaction=nonstopmode -file-line-error main.tex
    xelatex -interaction=nonstopmode -file-line-error main.tex
}
if (Test-Path main.pdf) { Copy-Item main.pdf TIEU_LUAN_NLP_RAG_FINAL.pdf -Force }
