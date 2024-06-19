#!/usr/bin/env bash

if [ $# -eq 0 ];
then
  echo "Running experiments with third-party system comparison ENABLED."
  echo "(Please make sure that SkinnerDB/MT and Postgres were installed properly.)"
else
  echo "Running experiments with third-party system comparison DISABLED."
    echo "(Only basic DuckDB/POLAR installation required.)"
fi

start=`date +%s`
source venv/bin/activate
python3 experiments/run1ExperimentPotentialBenefit.py
python3 experiments/run2ExperimentMicroBenchmarks.py
if [ $# -eq 0 ];
then
  python3 experiments/run3ExperimentEndToEnd.py
else
  python3 experiments/run3ExperimentEndToEndStatic.py
fi

mkdir -p paper/figures
mkdir -p paper/tables
cp static/figures/join_order_search_space-3.pdf paper/figures
cp static/figures/parallel-exec-2-2.pdf paper/figures
cp static/figures/polar_pipeline-5.pdf paper/figures
cp static/figures/routing_example.pdf paper/figures

python3 experiments/plot/plot_1_2_potential_savings.py
python3 experiments/plot/plot_2_0_sample_size.py
python3 experiments/plot/plot_2_1_enumeration_intms.py
python3 experiments/plot/plot_2_2_enumeration_timings.py
python3 experiments/plot/plot_2_3_routing_adaptive.py
python3 experiments/plot/plot_2_4_routing_all.py
python3 experiments/plot/plot_2_5_init_tuple.py
python3 experiments/plot/plot_3_1_pipeline.py
python3 experiments/plot/plot_3_2_query.py
python3 experiments/plot/plot_3_5_intermediates.py
python3 experiments/plot/plot_4_1_endtoend.py

cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
cd ..

end=`date +%s`
runtime=$((end-start))
echo "Experiment duration: ${runtime} seconds"