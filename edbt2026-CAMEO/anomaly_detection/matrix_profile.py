import os
import numpy as np
import time
import stumpy
from stumpy import core, config
from numba import set_num_threads

config.STUMPY_THREADS_PER_BLOCK = 1024
set_num_threads(4)


def top_k_discords(T, m, finite=False):
    excl_zone = int(np.ceil(m / config.STUMPY_EXCL_ZONE_DENOM))

    mp = stumpy.stump(T.astype(np.float64), m)
    P = mp[:,0].astype(np.float64)

    if finite:
        P[~np.isfinite(P)] = np.NINF

    discords_idx = np.full(1, -1, dtype=np.int64)
    discords_dist = np.full(1, np.NINF, dtype=np.float64)
    discords_nn_idx = np.full(1, -1, dtype=np.int64)

    mp_discord_idx = np.argmax(P)

    discords_idx[0] = mp_discord_idx
    discords_dist[0] = P[mp_discord_idx]
    discords_nn_idx[0] = mp[mp_discord_idx, 1]

    core.apply_exclusion_zone(P, discords_idx[0], excl_zone, val=np.NINF)

    out = np.empty((1, 3), dtype = object)
    out[:, 0] = discords_idx
    out[:, 1] = discords_dist
    out[:, 2] = discords_nn_idx

    return out


def detect_anomalies(new_tsf):
    overall_tp = 0

    min_m = 75
    max_m = 125

    for index, row in new_tsf.iterrows():
        ts = row.series
        end_training = row.end_training
        start_disc = row.start_disc
        end_disc = row.end_disc
        length = end_disc - start_disc

        all_discords_distance = []
        all_discords_indices = []
        for m in range(min_m, max_m + 1):
            top_k = top_k_discords(ts, m)[0]
            all_discords_indices.append(top_k[0])
            all_discords_distance.append(top_k[1])

        idx = all_discords_indices[np.argmax(all_discords_distance)]

        score = (
            1
            if min(start_disc - length, start_disc - 100) < idx + end_training < max(end_disc + length, end_disc + 100)
            else 0
        )

        overall_tp += score

    print('****Overall UCR-Score****', overall_tp / new_tsf.shape[0])

