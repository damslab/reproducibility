## Reproducibility Submission BTW 2025, Paper 150

**Authors:** Blagov, Kristiyan, Carlos Enrique Muñiz-Cuza, and Matthias Boehm

**Paper Name:** Fast, Parameter-Free Time Series Anomaly Detection

This repository contains the code to reproduce the results from the publication:

**Paper Links:**
 * <https://mboehm7.github.io/resources/btw2025a.pdf> (green open access)


Source Code Info
- **Standalone Implementation**: `stand_alone/stan.py`
- **Benchmark Integration**: `is-it-worth-it-benchmark/utsadbench/`
- **Programming Language**: Python

### Step-by-step Execution

#### 1. Install UCR Anomaly Archive & MERLIN 3.1

Download the [UCR Anomaly Archive and MERLIN](https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/) by running:

```bash
chmod +x ./scripts/install_merlin_ucr.sh
./install_merlin_ucr.sh
```

#### 2. Install Python Dependencies

STAN requires the following Python libraries:

```bash
pip install numpy scipy statsmodels scikit-learn tqdm
```

Alternatively, install from the provided requirements file:

```bash
pip install -r requirements/stan_alone_requirements.txt
```

#### 3. Run STAN

Once dependencies are installed, execute:

```bash
python stan_alone/stan.py
```

Run STAN using `alternative` subsequence size computation methods to reproduce Figure 8.

```bash
python stan_alone/stan.py alternative
```

Run STAN using the `aggregates` functions individually to reproduce Figure 5.

```bash
python stan_alone/stan.py aggregates
```

Run STAN using the aggregating function in an `incremental` way to reproduce Figure 6.

```bash
python stan_alone/stan.py incremental
```

### 4. Run MERLIN 3.1

MERLIN 3.1 requires MATLAB Engine API for Python. Follow [these instructions](https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html) to install it. Once installed, run:

```bash
python stan_alone/merlin.py
```

#### Potential Issues with MERLIN 3.1

- If using MATLAB R2020b or higher, update `nanmean` and `nanstd` in `MERLIN3_1.m` to:
  ```matlab
  mean(T, 'omitnan');
  std(T, 'omitnan');
  ```
- **`"Proceed with data modification? [y/n]";`**
  
  We set this option to `true` by default, letting MERLIN add a linear trend to solve issues related to near constant values. Simply comment out the while loop that expects the user answer and set the answer to "y" 
  ```matlab
  answer = "y";	% Set the answer to yes
  % while strcmp(answer,"y") == 0 && strcmp(answer,"n") == 0
      % answer = input(userQuestion, 's');
  % end
  ```
 
- Tested only on Windows 11.

### 4. Run Rest of the Baselines

We compare STAN with other baselines from the `utsadbench` framework, as introduced in:

> Ferdinand Rewicki, Joachim Denzler, and Julia Niebling. 2023. "Is It Worth It? Comparing Six Deep and Classical Methods for Unsupervised Anomaly Detection in Time Series." *Applied Sciences* 13(3): 1778. [DOI](https://doi.org/10.3390/app13031778)

#### Installing `utsadbench`

We recommend using [Anaconda](https://www.anaconda.com/download/) to create an isolated environment. To install all dependencies, run:

```bash
chmod +x install_utsadbench.sh
./install_utsadbench.sh
```

#### Running `utsadbench`

1. **Start the MLflow Server:**
   ```bash
   mkdir -p out/mlflow 
   mlflow server --host 0.0.0.0 -p 5000 --backend-store-uri sqlite:///out/mlflow/mlflow.sqlite --default-artifact-root $PWD/out/mlflow/artifacts/ --gunicorn-opts "--timeout 180"
   ```
2. **Run Experiments:**
   ```bash
   python utsadbench/experiments/main.py +experiment=main/<model>
   ```
   Replace `<model>` with `ae, ganf, mdi, rrcf, tranad`, and `merlin` (the results can diverge from the results reported using `MERLIN3_1.m`).

For hyperparameter tuning and additional details, see [`README.md`](is-it-worth-it-benchmark/README.md).

#### Building `MDI`

To build the MDI algorithm, ensure the following dependencies are installed:

- **gcc** (tested with g++ 9.4.0)
- **cmake** (tested with 3.31.5)
- **Eigen3** (tested with 3.4)
- **pkg-config** (tested with 0.29.1)
- **OpenMP** (tested with 4.5)
- **CUDA** (Version 12.2)

Once dependencies are installed, build `libmaxdiv` with:

```bash
cd is-it-worth-it-benchmark
chmod +x ./scripts/install_mdi.sh
./scripts/install_mdi.sh
```

#### Potential Issues with `utsadbench`

- **`AttributeError: module 'numpy' has no attribute 'bool'`**
  - Solution: Edit `is-it-worth-it-benchmark/utsadbench/results/classifier.py`, line 50:
    ```python
    bool  # Replace np.bool with bool
    ```

- **`No package 'eigen3' found --> Fatal error: Eigen/Core: No such file or directory`**
  - Solution: Install Eigen3 and update the `install_mdi.sh` script (line 22):
    ```bash
    cmake -D CMAKE_CXX_FLAGS=-I$EIGEN_HOME ..
    ```

- **`RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!`**
    - Solution: Edit `is-it-worth-it-benchmark/lib/tranad/main.py`, line 308 and line 330:
        ```python
        # Add these two lines of code to move the input data to the 
        # model's device while training and predicting.
        device = next(model.parameters()).device
        window, elem = window.to(device), elem.to(device)
        ```
- **`TypeError: can't convert cuda:0 device type tensor to numpy.`** 
    - Solution: Edit `is-it-worth-it-benchmark/lib/tranad/main.py` line 336:
        ```python
        # replace return statement
        return loss.detach().cpu().numpy(), z.detach().cpu().numpy()[0]
        ```
- **`TypeError: forward() got an unexpected keyword argument 'is_causal'`**
    - Solution: Edit `is-it-worth-it-benchmark/lib/tranad/src/dlutils.py`, line 270:
        ```python
        def forward(self, src, src_mask=None, src_key_padding_mask=None, **kwargs): # add **kwargs
        ```

### 5. Plot the Figures

We have provided the folder `plot_figures` with a python script per figure in the paper. For example, to reproduce figure 5 simply run:

```bash
python plot_figures/plot_fig_5.py
```

We have also provided a folder containing the artifacts produced by mlflow running the baselines. To generate results using the artifacts simply run:

```bash
python plot_figures/plot_fig_3_from_artifacts.py
```

## License

This repository is licensed under the [Apache 2.0](LICENSE) license.
