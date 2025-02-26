import os
import json
import pandas
from glob import glob
from tqdm import tqdm
import requests

byte_counts = {
    'I64': 8,
    'I32': 4,
    'BF16': 2,
    'I8': 1,
    'F8_E4M3': 1,
    'F8_E5M2': 1,
}

model_sizes = {}

def parse_model_args(model_args):
    if "deltazip" in model_args:
        model_args = model_args.split("deltazip")[1]
        model_args = model_args.split(",")[0]
        model_args = model_args.strip(".")
        model_args = model_args.replace(".", "/")
    if "espressor" in model_args:
        model_args = model_args.split("espressor/")[1]
        model_args = model_args.split(",")[0]
        model_args = model_args.strip(".")
        model_args = model_args.replace(".", "/",1)
        model_args = model_args.split("_")[0]
    else:
        model_args = model_args.split(",")[0]
        model_args = model_args.replace("pretrained=", "")
    return model_args

def get_hf_name(model_args):
    model_args = model_args.split("pretrained=")[1]
    model_args = model_args.split(",")[0]
    return model_args

def get_hf_size(hf_name):
    if hf_name in model_sizes:
        return model_sizes[hf_name]
    else:
        api_endpoint = f"https://huggingface.co/api/models/{hf_name}?blobs=true"
        response = requests.get(api_endpoint).json()
        safetensors_data = response['safetensors']['parameters']
        total_bytes = sum([byte_counts.get(dtype, 0) * size for dtype, size in safetensors_data.items()])
        model_sizes[hf_name] = total_bytes
        return total_bytes

def parse_model_precision(model_args):
    if "espressor" in model_args:
        if 'W8A8_int8' in model_args:
            precision = 'W8A8_int8'
        elif 'W4A16' in model_args:
            precision = 'W4A16'
        elif 'FP8' in model_args:
            precision = 'W8A8_FP8'
        else:
            raise ValueError(f"Unknown precision: {model_args}")
    else:
        precision = "Default (bf16/fp16)"
    return precision

def parse_lmeval(args):
    print(args)
    result_files = [y for x in os.walk(args.input) for y in glob(os.path.join(x[0], '*.json'))]
    print(f"Found {len(result_files)} result files")
    results = []
    for rf in tqdm(result_files):    
        with open(rf, 'r') as f:
            data = json.load(f)
            config = data['config']
            data = data['results']
            for task, eval_res in data.items():
                for eval_key, eval_val in eval_res.items():
                    if eval_key!= 'alias':
                        precision = parse_model_precision(config['model_args'])
                        results.append({
                            'model': parse_model_args(config['model_args'])+":"+precision,
                            'task': 'task_'+task,
                            'metric': eval_key.replace(',none', ''),
                            'value': eval_val,
                            'precision': precision,
                            'hf_name': get_hf_name(config['model_args']),
                            'model_physical_size': get_hf_size(get_hf_name(config['model_args'])),
                        })
    df = pandas.DataFrame(results)
    # take acc only
    df = df[df['metric'] == 'acc']
    df.to_csv('.local/eval_results.csv', index=False)

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='.local/eval_results')
    parser.add_argument("--output", type=str, default='.local/eval_results.csv')
    args = parser.parse_args()
    parse_lmeval(args)