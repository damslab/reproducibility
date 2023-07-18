all: create clean

create:	
	pdflatex -shell-escape exp1_micor_bench_identification.tex
	pdflatex -shell-escape exp2_identification_1k_10k_Table3.tex
	pdflatex -shell-escape exp3_early.tex
	pdflatex -shell-escape exp4_micro_bench.tex
	pdflatex -shell-escape exp5_systematic.tex
	pdflatex -shell-escape exp6_end_to_end.tex

clean:
	rm -rf *.aux  *.nav  *.vrb  *.log  *.out *.snm *.toc *.gz *.mtc* *.maf *.fls *.tmp *.bbl *.blg  *.mtc  *.bcf *.xml *.fdb_latexmk plots/*.dep plots/*.dpth plots/*.log plots/*.md5 *.auxlock exp1_micor_bench_identification.pdf exp3_early.pdf exp4_micro_bench.pdf exp5_systematic.pdf exp6_end_to_end.pdf

