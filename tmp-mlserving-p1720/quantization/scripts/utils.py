import json
import copy
import torch
import random
import datasets
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from glob import glob
from typing import List
from pathlib import Path
from scratchpad.utils.client import LLM
from scratchpad.extensions.shepherd import Route, create_route_from_results


def set_matplotlib_style():
    pd.set_option("display.max_columns", 500)
    sns.set_style("ticks")
    font = {
        # "font.family": "Roboto",
        "font.size": 12,
    }
    sns.set_style(font)
    paper_rc = {
        "lines.linewidth": 3,
        "lines.markersize": 10,
    }
    sns.set_context("paper", font_scale=2, rc=paper_rc)
    matplotlib.rcParams["pdf.fonttype"] = 42
    matplotlib.rcParams["ps.fonttype"] = 42
    sns.set_theme(style="whitegrid")

def autolabel(rects, ax, prec=1):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f"{height:.{prec}f}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            size=9,
        )
        
answer_mapping = ["A", "B", "C", "D"]

model_mappings = {
    "meta-llama/Llama-3.2-1B-Instruct": LLM(
        model="meta-llama/Llama-3.2-1B-Instruct",
        base_url="http://localhost:8081/v1",
        api_key="test",
    ),
    "meta-llama/Llama-3.2-3B-Instruct": LLM(
        model="meta-llama/Llama-3.2-3B-Instruct",
        base_url="http://localhost:8082/v1",
        api_key="test",
    ),
    "meta-llama/Llama-3.1-8B-Instruct": LLM(
        model="meta-llama/Llama-3.1-8B-Instruct",
        base_url="http://localhost:8083/v1",
        api_key="test",
    ),
    "meta-llama/Llama-3.3-70B-Instruct": LLM(
        model="meta-llama/Llama-3.3-70B-Instruct",
    ),
}
# cheapest pricing from openrouter.ai for bf16, per million tokens
pricings = {
    "meta-llama/Llama-3.2-1B-Instruct": 0.01,
    "meta-llama/Llama-3.2-3B-Instruct": 0.015,
    "meta-llama/Llama-3.1-8B-Instruct": 0.025,
    "meta-llama/Llama-3.3-70B-Instruct": 0.39,
}
penalty = torch.tensor([pricings[model] for model in model_mappings.keys()])
penalty = penalty / penalty.sum()


def create_route_from_file(
    jsonl_path: str, downsample_factor=1, cascade=True
) -> List[Route]:
    return create_route_from_results(
        jsonl_path,
        answer_mapping=answer_mapping,
        model_mapping=model_mappings,
        build_prompt=build_prompt,
        downsample_factor=downsample_factor,
        cascade=cascade,
    )


def calculate_llms_accuracy(data):
    models = data[0]["output"].keys()
    accuracies = {}
    for model in models:
        correct = 0
        for row in data:
            if answer_mapping[row["answer"]] == row["output"][model]:
                correct += 1
        accuracies[model] = correct / len(data)
    return accuracies


def build_prompt(row):
    """ """
    user_prompt = (
        f"{row['question']}\n"
        + "\n".join(
            [
                f"{choice}. {answer}"
                for choice, answer in zip(answer_mapping, row["choices"])
            ]
        )
        + "\nAnswer:"
    )
    row["prompt"] = user_prompt
    return row


def construct_ds(test_ratio: float = 0.2, seed=42):
    random.seed(seed)
    dataset = datasets.load_dataset("cais/mmlu", "all")["test"]
    dataset = dataset.shuffle(seed=seed)
    results = dataset.train_test_split(test_size=test_ratio)

    train, test = results["train"], results["test"]
    train = train.map(lambda x: build_prompt(x))
    test = test.map(lambda x: build_prompt(x))
    return train, test


def load_test_set():
    with open(".local/shepherd/llm_responses_test.jsonl", "r") as f:
        data = [json.loads(line) for line in f]
    return data

def decontamination(test, train):
    # return a new trainset that does not include any contamination
    formatted_train = [f"{t['subject']} {t['question']} {t['choices']}" for t in train]
    formatted_test = [f"{t['subject']} {t['question']} {t['choices']}" for t in test]
    new_train = []
    for t in formatted_train:
        if t not in formatted_test:
            new_train.append(train[formatted_train.index(t)])
    return new_train

def check_contamination(test, train):
    formatted_train = [f"{t['subject']} {t['question']} {t['choices']}" for t in train]
    formatted_test = [f"{t['subject']} {t['question']} {t['choices']}" for t in test]
    for t in formatted_test:
        if t in formatted_train:
            print(f"Found contamination: {t}")
            return True
    return False