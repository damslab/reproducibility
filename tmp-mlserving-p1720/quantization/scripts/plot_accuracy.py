import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.utils import set_matplotlib_style, autolabel

set_matplotlib_style()

def plot_accuracy(acc_df):
    # Tasks to plot and model variants to consider
    tasks = ['task_openbookqa', 'task_mmlu', 'task_truthfulqa_mc2', 'task_boolq', 'task_logiqa']
    base_model = "meta-llama/Llama-3.1-8B-Instruct"
    # Variants in desired order
    variants = ["Default (bf16/fp16)", "W8A8_int8", "W8A8_FP8", "W4A16"]
    # Construct full model id names corresponding to model column in CSV
    model_ids = [f"{base_model}:{v}" for v in variants]

    # Filter dataframe to include only the model ids and tasks of interest
    sub_df = acc_df[acc_df["model"].isin(model_ids)]
    plot_df = sub_df[sub_df["task"].isin(tasks)].copy()
    # Extract the variant name from the model column (using the colon as the separator)
    plot_df["variant"] = plot_df["model"].str.split(":").str[1]
    
    # Compute the baseline accuracy for each task using the default variant.
   
    baseline = plot_df[plot_df["variant"] == "Default (bf16/fp16)"].set_index("task")["value"].to_dict()
    # Create a new column "relative" by dividing each accuracy value by the baseline for that task.
    plot_df["relative"] = plot_df.apply(lambda row: row["value"] / baseline[row["task"]], axis=1)
    plot_df['task'] = plot_df['task'].str.replace('task_', '')
    plot_df['task'] = plot_df['task'].str.replace('_mc2', '')
    tasks = plot_df["task"].unique() 
    # Create a single grouped bar plot:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=plot_df,
                x="task",
                y="relative",
                hue="variant",
                order=tasks,
                hue_order=variants)
    plt.ylim(0.75, 1.1)
    plt.xlabel("Task")
    # enlarge font ticks
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    # enlarge font labels
    plt.xlabel("Task", fontsize=16)
    plt.ylabel("Relative Accuracy", fontsize=16)
    plt.ylabel("Relative Accuracy")
    plt.title("Relative Accuracy of Model Variants on Different Tasks")
    plt.legend(title="Variant", bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=4)
    plt.tight_layout()
    sns.despine()
    plt.savefig("accuracy_single_plot.pdf")
    plt.show()
    
if __name__=="__main__":
    acc_df = pd.read_csv(".local/eval_results.csv")
    plot_accuracy(acc_df)