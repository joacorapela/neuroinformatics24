all: worksheet_linearDynamicalSystems.pdf

%.pdf: %.tex
	pdflatex $<*
	bibtex $*.aux
	pdflatex $<*
	pdflatex $<*

