import os
import pandas as pd
import shutil
from os import path, remove
import pyarrow as pa
import pyarrow.parquet as pq
import subprocess


def read_metadata(path_to_meta):
    r_map = {}
    with open(path_to_meta) as _file:
        for i, line in enumerate(_file):
            if i >= 5:
                n, label = line.split()
                label = label.split('-')[1].replace('.0', '')
                r_map[int(n)] = label
    return r_map


class ModelCompressor:
    coefficients = [1.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0]
    ped_pmc_error_bounds = [100.0, 200.0, 300.0, 400.0, 500.0]
    ped_swing_error_bounds = [10.0, 30.0, 50.0, 70.0, 90.0]
    
    name_map_coef = {'pmc': ped_pmc_error_bounds, 'swing': ped_swing_error_bounds}

    jar_file = "compression/ModelarDB.jar"
    main_class = "compression/ModelarDBRunner.java"
    model_map = {'pmc': 'C', 'swing': 'L', 'sp': 'S'}

    def __init__(self, ts, data_name):
        self.data_name = data_name
        self.src = f'data/raw/{data_name}.parquet'
        os.makedirs(f'data/raw/', exist_ok=True)
        date = pd.date_range('2000/01/01', periods=len(ts), freq='min')
        df = pd.DataFrame()
        df['datetime'] = date
        df['y'] = ts
        table = pa.Table.from_pandas(df, schema=pa.schema([
            ('datetime', pa.timestamp('us')),
            ('y', pa.float32())  # Casting 'y' to float32 
        ]))

        # Write the table to a Parquet file
        pq.write_table(table, self.src)
    

    def compress(self, model, fraction):
        os.makedirs(f'data/compressed/{model}/error_bound_{fraction}/', exist_ok=True)

        segments_dst = f'data/compressed/{model}/error_bound_{fraction}/partial_{self.data_name}_segments_{model}.parquet'
        
        process = subprocess.run(['java', '-cp', self.jar_file, self.main_class, self.src, str(fraction), self.model_map[model]],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = process.stdout.decode('utf-8')
        stderr = process.stderr.decode('utf-8')

        if process.returncode != 0:
            print(f'There was an error: {stderr}')
        else:
            print(f'Output: {stdout}')

        if path.exists(segments_dst):
            segments_df = pd.read_parquet(segments_dst)
        else:
            raise Exception(f"File not found... ({segments_dst})")

        return segments_df

    def decompress(self, model, fraction):
        decomp_rep = pd.read_parquet(f'data/compressed/{model}/error_bound_{fraction}/partial_{self.data_name}_points_{model}.parquet')
            
        return decomp_rep[f'y-E{fraction}'].values













