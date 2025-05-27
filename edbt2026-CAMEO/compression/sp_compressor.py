import tersets
import numpy as np
import os


class SimPiece():
    error_bounds = np.arange(0.01, 1.005, 0.01)
    ped_sp_error_bounds = [0.01, 0.03, 0.05, 0.07, 0.1, 0.13, 0.15, 0.17, 0.2]
    def __init__(self):
        super().__init__()

    def compress(self, uncompressed, error_bound, fh=None, index=None):
        return np.asarray(tersets.compress(uncompressed, tersets.Method.SimPiece, error_bound))
        
    def decompress(self, compressed):
        if isinstance(compressed, np.ndarray):
            return tersets.decompress(compressed.tolist())
        return tersets.decompress(compressed)
        
    


    