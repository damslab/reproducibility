import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from transformers import AutoTokenizer

from scripts.utils import (
    build_prompt,
    answer_mapping,
    pricings,
    set_matplotlib_style
)

model_name_mapping = {
    "meta-llama/Llama-3.2-1B-Instruct": "3.2-1B",
    "meta-llama/Llama-3.2-3B-Instruct": "3.2-3B",
    "meta-llama/Llama-3.1-8B-Instruct": "3.1-8B",
    "meta-llama/Llama-3.3-70B-Instruct": "3.3-70B",
    "router": "Router",
}


def plot_cost_accuracy(results):
    set_matplotlib_style()
    # rename models
    results["model"] = results["model"].map(model_name_mapping)
    models = results["model"]

    cost_values = np.array(results["cost"])
    accuracy_values = np.array(results["accuracy"])
    norm_cost = cost_values / max(cost_values)
    norm_acc = accuracy_values / max(accuracy_values)
    # Create positions for grouped bars
    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width / 2, norm_cost, width, label="Normalized Cost")
    ax.bar(x + width / 2, norm_acc, width, label="Normalized Accuracy")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_title("Model Performance: Normalized Cost and Accuracy")
    ax.legend()
    # set y-axis to be log-scale

    sns.despine()
    plt.savefig(".local/shepherd/router_stats.pdf")
    plt.show()


def plot(args):
    print(args)
    df = pd.read_csv(args.result_file)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    results = []
    with open(args.test_data) as f:
        test_data = [json.loads(line) for line in f]
    for model in pricings.keys():
        correct_answers = []
        model_answers = []
        prompts = []
        for row in test_data:
            user_prompt = build_prompt(row)["prompt"]
            correct_answer = answer_mapping[row["answer"]]
            model_answer = row["output"][model]
            prompts.append(user_prompt)
            correct_answers.append(correct_answer)
            model_answers.append(model_answer)
        accuracy = sum(
            [1 for i, j in zip(correct_answers, model_answers) if i == j]
        ) / len(correct_answers)
        total_tokens = sum([len(tokenizer.encode(prompt)) for prompt in prompts])
        cost = pricings[model] * total_tokens
        print(f"Model: {model}, Accuracy: {accuracy}, Total cost: {cost}")
        results.append(
            {
                "model": model,
                "accuracy": accuracy,
                "cost": cost,
            }
        )

    prompts = []
    correct_answers = []
    model_answers = []
    costs = []
    # now process router
    for index, row in df.iterrows():
        subject = row["subject"]
        question = row["question"]
        # find the raw data from data_data
        datum = [
            x
            for x in test_data
            if x["subject"] == subject and x["question"] == question
        ][0]
        user_prompt = build_prompt(datum)["prompt"]
        correct_answer = answer_mapping[datum["answer"]]
        model_answer = row["router_response"]
        correct_answers.append(correct_answer)
        model_answers.append(model_answer)
        selected_model = row["router_selected_model"]
        cost = pricings[selected_model] * len(tokenizer.encode(user_prompt))
        costs.append(cost)
    accuracy = sum([1 for i, j in zip(correct_answers, model_answers) if i == j]) / len(
        correct_answers
    )
    cost = sum(costs)
    print(f"Router Accuracy: {accuracy}, Total cost: {cost}")
    results.append(
        {
            "model": "router",
            "accuracy": accuracy,
            "cost": cost,
        }
    )

    results = pd.DataFrame(results)
    results.to_csv(".local/routing/plot_router_stats.csv", index=False)

    # plot the results
    set_matplotlib_style()
    plot_cost_accuracy(results)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result-file", type=str, default=".local/shepherd/router_results.csv"
    )
    parser.add_argument(
        "--test-data", type=str, default=".local/shepherd/llm_responses_test.jsonl"
    )
    parser.add_argument(
        "--tokenizer", type=str, default="meta-llama/Llama-3.2-1B-Instruct"
    )
    plot(parser.parse_args())
