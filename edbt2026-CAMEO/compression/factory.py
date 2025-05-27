import os
import numpy as np
import pandas as pd
import pickle as pkl
from compression import \
    frequency_compressors, \
        line_simplification, \
                sp_compressor, \
                    segmentation_compressor, \
                        model_compressor

class CompressorFactory(object):
    _shared_borg_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(CompressorFactory, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_borg_state
        return obj

    # def __init__(self, name=None):
    #     self.__compression_name = name

    @staticmethod
    def get_compressor(compression_name):
        if compression_name == "dft":
            return frequency_compressors.DFTCompressor()
        elif compression_name == "dwt":
            return frequency_compressors.DWTCompressor()
        elif compression_name == 'cameo':
            return line_simplification.LineSimplification()
        elif compression_name == 'vw':
            return line_simplification.LineSimplification()
        elif compression_name == 'pip':
            return line_simplification.LineSimplification()
        elif compression_name == 'tp':
            return line_simplification.LineSimplification()
        elif compression_name == 'pmc':
            return model_compressor.ModelCompressor()
        elif compression_name == 'swing':
            return model_compressor.ModelCompressor()
        elif compression_name == 'sp':
            return sp_compressor.SimPiece()
        elif compression_name == 'swab':
            return segmentation_compressor.SWAB()
        elif compression_name == 'ped_mae_cameo':
            return line_simplification.LineSimplification()
        elif compression_name == 'ped_rmse_cameo':
            return line_simplification.LineSimplification()
        elif compression_name == 'ped_cheb_cameo':
            return line_simplification.LineSimplification()
        else:
            raise ValueError("Invalid compression type")

    @staticmethod
    def exists(compression, data_name, fraction):
        if os.path.exists(os.path.join('data', 'compressed', compression,
                                       f'num_coef_{fraction}', f'{data_name}_compressed')):
            os.rename(os.path.join('data', 'compressed', compression,
                                   f'num_coef_{fraction}', f'{data_name}_compressed'),
                      os.path.join('data', 'compressed', compression,
                                   f'num_coef_{fraction}', f'{data_name}_compressed.pkl'))
            return True

        if os.path.exists(os.path.join('data', 'compressed', compression,
                                       f'num_coef_{fraction}', f'{data_name}_compressed.npy')):
            data = np.load(os.path.join('data', 'compressed', compression,
                                        f'num_coef_{fraction}', f'{data_name}_compressed.npy'), allow_pickle=True)
            with open(os.path.join('data', 'compressed', compression,
                                   f'num_coef_{fraction}', f'{data_name}_compressed.pkl'), 'wb') as f:
                pkl.dump(data, f)

            os.remove(os.path.join('data', 'compressed', compression,
                                   f'num_coef_{fraction}', f'{data_name}_compressed.npy'))

        if os.path.exists(os.path.join('data', 'compressed', compression,
                                       f'num_coef_{fraction}', f'{data_name}_compressed.txt')):

            with open(os.path.join('data',
                                   'compressed', compression, f'num_coef_{fraction}',
                                   f'{data_name}_compressed.txt'), 'r') as f:
                new_data = [np.asarray([float(num) for num in line.split(',')]) for line in f]

            with open(os.path.join('data',
                                   'compressed', compression, f'num_coef_{fraction}',
                                   f'{data_name}_compressed.pkl'), 'wb') as f:
                pkl.dump(new_data, f)

            os.remove(os.path.join('data', 'compressed', compression,
                                   f'num_coef_{fraction}', f'{data_name}_compressed.txt'))

        return os.path.exists(os.path.join('data', 'compressed', compression,
                                           f'num_coef_{fraction}', f'{data_name}_compressed.pkl'))

    @staticmethod
    def load_data(compression, data_name, index, fraction):
        p = os.path.join('data', 'compressed', compression,
                         f'num_coef_{fraction}', f'{data_name}_compressed.pkl')
        try:
            with open(p, 'rb') as f:
                return pkl.load(f)[index]
        except IndexError as excp:
            print(excp)
            p = os.path.join('data', 'compressed', compression,
                             f'num_coef_{fraction}', f'{data_name}_segments_{compression}.parquet')
            df = pd.read_parquet(p)
            return df[df.gid == index]


    @staticmethod
    def save_data(x, compression, data_name, fraction):
        p = os.path.join('data', 'compressed', compression,
                         f'num_coef_{fraction}', f'{data_name}_compressed.pkl')
        os.makedirs(os.path.join('data', 'compressed', compression, f'num_coef_{fraction}'), exist_ok=True)
        with open(p, 'wb') as f:
            pkl.dump(x, f)
