all: worksheet_circularStatistics.pdf

%.pdf: %.tex
	pdflatex $<*
	bibtex $*.aux
	pdflatex $<*
	pdflatex $<*

