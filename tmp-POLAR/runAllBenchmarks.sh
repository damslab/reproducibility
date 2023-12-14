#!/usr/bin/env bash

start=`date +%s`
source venv/bin/activate
python3 experiments/run1ExperimentPotentialBenefit.py
python3 experiments/run2ExperimentMicroBenchmarks.py
python3 experiments/run3ExperimentEndToEndStatic.py

mkdir -p paper/figures
mkdir -p paper/tables

python3 experiments/plot/plot_1_2_potential_savings.py
python3 experiments/plot/plot_2_1_enumeration_intms.py
python3 experiments/plot/plot_2_2_enumeration_timings.py
python3 experiments/plot/plot_2_3_routing_adaptive.py
python3 experiments/plot/plot_2_4_routing_all.py
python3 experiments/plot/plot_3_1_pipeline.py
python3 experiments/plot/plot_3_2_query.py
python3 experiments/plot/plot_4_1_endtoend_static.py

# cd paper
# pdflatex -interaction=nonstopmode main.tex
# bibtex main
# pdflatex -interaction=nonstopmode main.tex
# pdflatex -interaction=nonstopmode main.tex
# cd ..

end=`date +%s`
runtime=$((end-start))
echo "Experiment duration: ${runtime} seconds"