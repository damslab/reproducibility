import numpy as np
import os
import time
import matlab.engine
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm


def ucr_score(anomaly_idx, begin, end, length):
    return min(begin - length, begin - 100) < anomaly_idx < max(end + length, end + 100)


def run_merlin(ts, start_training, eng):
    scaler = MinMaxScaler()
    test_ts = scaler.fit_transform(ts[start_training:].reshape(-1, 1)).flatten()
    
    eng.addpath(os.path.join(os.getcwd(), "stan_alone"))
    distance, indices, length = eng.MERLIN3_1(test_ts, float(75), float(125), False, nargout=3)
    

    # Convert each MATLAB array individually to a NumPy array
    indices = np.array(indices._data).reshape(indices.size, order='F')  # MATLAB uses column-major order
    

    indices = np.sort(np.squeeze(indices)) # Sort results to find middle discord with most neighbors
    diff_matrix = np.abs(indices[:, None] - indices)  # Compute absolute differences
    count_list = np.sum(diff_matrix <= 100, axis=1) - 1  # Count neighbors (excluding self)
    max_discords = np.where(count_list == np.max(count_list))[0] # Find discord with most neighbors
    discord_index = indices[max_discords[len(max_discords) // 2]] # Return middle discord with most neighbors
    discord_index += start_training # Add start_training to get correct index
    return int(discord_index)


def run_experiments_ucr(memory=True):
    ucraa_root = os.path.join(os.getcwd(), "data", "ucraa")
    files = sorted([f for f in os.listdir(ucraa_root) if os.path.isfile(os.path.join(ucraa_root, f))])
    name_time_series_list = []
    time_series_list = []
    ucr_results = []

    if memory:
        try:
            ucr_results = np.fromfile(os.path.join(os.getcwd(), "results", "merlin_ucr_results.txt"), sep="\n")
            print(f"Results loaded from memory. Running experiments from file {ucr_results.shape[0]}" )
            print("Deactivate memory to rerun experiments from scratch.")
            files = files[ucr_results.shape[0]:]
            ucr_results = ucr_results.tolist()
        except:
            print("No results found in memory. Running experiments from scratch...")

    print("Loading data...")
    for file in tqdm(files):
        if file.endswith(".txt"):
            ts = np.fromfile(os.path.join(ucraa_root, file), sep="\n")
            if ts.shape[0] < 100:
                ts = np.fromfile(os.path.join(ucraa_root, file), sep=" ")
            time_series_list.append(ts)
            name_time_series_list.append(file)
    
    start_time = time.time()
    idx = 0
    print("Detecting anomalies...")
    eng = matlab.engine.start_matlab()
    for ts in tqdm(time_series_list):
        ts_name = name_time_series_list[idx]
        parts = list(ts_name.split("_"))
        begin = int(parts[-2])
        end = int(parts[-1][:-4])
        start_training = int(parts[-3])
        anom_length = end-begin+1
        anomaly_idx  = run_merlin(ts, start_training, eng)
        ucr_results.append(ucr_score(anomaly_idx, begin, end, anom_length))
        np.savetxt(os.path.join(os.getcwd(), "results", "merlin_ucr_results.txt"), ucr_results, fmt='%d')
        idx += 1
    eng.quit()

    end_time = time.time()
    runtime = end_time - start_time
    print("UCR-Score:", np.mean(ucr_results)*100, f"% ({np.sum(ucr_results)}/250 correctly detected anomalies)")
    print("Total Runtime:", np.round(runtime, 2), "seconds")
    print("Runtime per Dataset:", np.round(runtime/250, 2), "seconds")
    print("Correctly detected anomalies per summary statistic:")

    np.savetxt(os.path.join(os.getcwd(), "results", "merlin_ucr_results.txt"), ucr_results, fmt='%d')
    np.savetxt(os.path.join(os.getcwd(), "results", "merlin_exec_time.txt"), np.array([np.round(runtime, 2), np.round(runtime/250, 2)]))


if __name__ == '__main__':
    run_experiments_ucr(memory=True)