all: circularVariablesStatExamples.pdf

%.pdf: *.tex
	pdflatex $<
	bibtex $*.aux
	pdflatex $<
	pdflatex $<
