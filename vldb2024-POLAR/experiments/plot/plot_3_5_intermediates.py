#!/usr/bin/env python3

import os
import pandas as pd

benchmarks = ["imdb", "ssb", "ssb-skew"]
systems = ["polar", "duckdb", "skinnerdb"]

results = {}
for system in systems:
    results[system] = {}
    for benchmark in benchmarks:
        if system == "skinnerdb" or system == "skinnermt":
            if benchmark != "imdb":
                continue
            path = os.getcwd() + f"/experiment-results/3_5_intermediates/{benchmark}/{system}/{system}-1.csv"
            df = pd.read_csv(path)
            df = df.groupby("Query").median()
            sum_intermediates = 0
            for index, row in df.iterrows():
                sum_intermediates += float(row["Tuples"])
            results[system][benchmark] = sum_intermediates
            continue

        path = os.getcwd() + f"/experiment-results/3_5_intermediates/{benchmark}/{system}/{system}.log"

        sum_intermediates = 0
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Join Intermediates:"):
                    sum_intermediates += int(line.split(" ")[-1])
        results[system][benchmark] = sum_intermediates

print(results)

formatted_results = {}
for system in systems:
    formatted_results[system] = {}
    for benchmark in benchmarks:
        if system == "skinnerdb" and benchmark != "imdb":
            continue
        formatted_results[system][benchmark] = "{:10.0f}".format(results[system][benchmark] / 1000000)

latex_table = f"""\\begin{{table}}
	\\centering
	\\caption{{Total Number of Intermediates ($C_{{out}}$) Comparison.}}
	 \\vspace{{-0.3cm}} 
  \\setlength\\tabcolsep{{14.7pt}}
   \\begin{{tabular}}{{lccc}}
	  \\toprule
        \\textbf{{System}} & \\textbf{{JOB}} & \\textbf{{SSB}} & \\textbf{{SSB-skew}} \\\\
        \\midrule
		DuckDB & {formatted_results["duckdb"]["imdb"]}\\,M & {formatted_results["duckdb"]["ssb"]}\\,M & {formatted_results["duckdb"]["ssb-skew"]}\\,M\\\\
        Postgres & 272\\,M & 598\\,M & 503\\,M\\\\
        SkinnerDB & {formatted_results["skinnerdb"]["imdb"]}\\,M & --- & ---\\\\
        \\midrule
        POLAR & {formatted_results["polar"]["imdb"]}\\,M & {formatted_results["polar"]["ssb"]}\\,M & {formatted_results["polar"]["ssb-skew"]}\\,M\\\\
		\\bottomrule
	\\end{{tabular}}
	\\label{{tab:3_5_intermediates}}
	\\vspace{{-0.2cm}}
\\end{{table}}
"""

with open(f"{os.getcwd()}/paper/tables/3_5_intermediates.tex", "w") as file:
    file.write(latex_table)
    file.flush()
