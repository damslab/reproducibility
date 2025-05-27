# CAMEO: Autocorrelation-preserving Line Simplification for Lossy Time Series Compression 

CAMEO is a lossy time series compression algorithm capable of 
preserving the AutoCorrelation Function (ACF) of the decompressed data within an error bound of the original ACF.
CAMEO efficiently re-computes the ACF by keeping basic aggregates. CAMEO is implemented in Cython to increase its efficiency, avoid python GIL constraints, and take full advantage
of multi-threading.  

This repository reproduces the results presented in the paper:

> Carlos sdj fijdf ijfd fdifjdif ijsdsd 

This is a work in progress. 

## Installation

Clone the repository:

```bash
git clone git@github.com:damslab/reproducibility.git
cd reproducibility/edbt2026-CAMEO
```

## Setting Up a Virtual Environment
(Optional but recommended) Set up a Anaconda virtual environment:

```bash
conda create --name cameo_env
conda activate cameo_en  # On Windows use `venv\Scripts\activate`
```
This way you can still all dependencies one by one. Another way is to create the environment directly using the provided `.yml`
## Installing Dependencies
Install the required Python package:
```bash
conda env create -f environment.yml
```

## Compiling Cython Code

Compile the Cython modules:

```bash
python setup.py build_ext --inplace
```

