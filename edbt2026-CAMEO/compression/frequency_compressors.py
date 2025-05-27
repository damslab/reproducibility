import numpy as np
from scipy.fftpack import dct, idct


class FreqComp:
    coefficients = [0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1]

    def compress(self, data, fraction, _=None, __=None):
        pass

    def decompress(self, compressed_data):
        pass


class DFTCompressor(FreqComp):
    def compress(self, data, fraction, _=None, __=None):
        dft_data = np.fft.fft(data)
        num_coefficients = int(len(data)*fraction)
        sorted_coefficients = np.argsort(np.abs(dft_data))[::-1]  # Sort coefficients by magnitude
        top_coefficients = sorted_coefficients[:num_coefficients]
        compressed_data = np.zeros(len(data), dtype=np.complex_)
        compressed_data[top_coefficients] = dft_data[top_coefficients]
        return compressed_data

    def decompress(self, compressed_data):
        return np.fft.ifft(compressed_data).real.tolist()


class DWTCompressor(FreqComp):
    def compress(self, data, fraction, _=None, __=None):
        # Apply DCT to data
        dct_coeffs = dct(data, type=2, norm='ortho')

        # Zero out a fraction of the highest frequency components
        num_coefficients = int(fraction * len(dct_coeffs))
        dct_coeffs[-num_coefficients:] = 0

        return dct_coeffs

    def decompress(self, compressed_data):
        # Apply inverse DCT
        data_reconstructed = idct(compressed_data, type=2, norm='ortho')

        return data_reconstructed




