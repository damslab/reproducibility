import re
import argparse
import matplotlib.pyplot as plt


def parse_benchmark_results(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    dp, tp, pp = None, None, None
    request_rate = None
    results = []
    
    for line in lines:
        # Match configuration
        config_match = re.match(r"\+{7} Running experiment with configuration: DP=(\d+), TP=(\d+), PP=(\d+)", line)
        if config_match:
            dp, tp, pp = map(int, config_match.groups())
            continue
        
        # Match request rate
        rate_match = re.match(r"\+{7} Running with request rate: (\d+)", line)
        if rate_match:
            request_rate = int(rate_match.group(1))
            continue
        
        # Match Request throughput
        throughput_match = re.match(r"Total Token throughput \(tok/s\):\s+([\d\.]+)", line)
        if throughput_match:
            request_throughput = float(throughput_match.group(1))
            continue
        
        # Match Mean TTFT
        ttft_match = re.match(r"Mean TTFT \(ms\):\s+([\d\.]+)", line)
        if ttft_match:
            mean_ttft = float(ttft_match.group(1))
            
            # Store results
            results.append((dp, tp, pp, request_rate, request_throughput, mean_ttft))
    
    # Print results
    for dp, tp, pp, request_rate, request_throughput, mean_ttft in results:
        print(f"DP={dp}, TP={tp}, PP={pp}, Request Rate={request_rate}")
        print(f"  Request Throughput: {request_throughput} req/s")
        print(f"  Mean TTFT: {mean_ttft} ms")
        print()

    request_rates = sorted(set(d[3] for d in results))
    strategies = sorted(set((d[0], d[1], d[2]) for d in results))  # Unique (DP, TP, PP) strategies

        # Generate separate scatter plots for each request rate
        # Define more distinct colors and markers
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'tab:orange', 'tab:purple', 'tab:brown']
    markers = ['o', 's', '^', 'D', 'P', '*', 'X', 'v', '<', '>']

    # Create a strategy mapping to assign unique color-marker pairs
    strategy_map = {strategy: (colors[i % len(colors)], markers[i % len(markers)]) for i, strategy in enumerate(strategies)}

    # Generate separate scatter plots for each request rate
    for request_rate in request_rates:
        plt.rcParams['lines.markersize'] = 12
        plt.figure(figsize=(8, 5))
        
        # Filter data for the specific request rate
        filtered_data = [d for d in results if d[3] == request_rate]
        
        # Plot each strategy with distinct color and marker
        for strategy in strategies:
            strat_data = [d for d in filtered_data if (d[0], d[1], d[2]) == strategy]
            if strat_data:
                x_vals = [d[4] for d in strat_data]  # Request Throughput
                y_vals = [d[5] for d in strat_data]  # Mean TTFT
                color, marker = strategy_map[strategy]
                plt.scatter(x_vals, y_vals, color=color, marker=marker, label=f"DP={strategy[0]}, TP={strategy[1]}, PP={strategy[2]}", alpha=0.7)

        # Adjust axes and increase marker size
        plt.xlim(left=0, right=1.15 * max(d[4] for d in filtered_data))
        plt.ylim(bottom=0, top=max(1.15 * min(d[5] for d in filtered_data), 1000))
        
        # Labels and title
        plt.xlabel("Throughput (Tokens)", fontsize=16)
        plt.ylabel("Latency (ms)", fontsize=16)
        # plt.title(f"Throughput vs. Latency (Request Rate={request_rate})")
        plt.grid(True)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        
        # Add legend
        plt.legend(loc="upper left", fontsize=11)
        
        # Display the plot
        plt.show()
        # Save plot instead of showing
        plt.savefig(f'hybrid_parallelism_plot_rate_{request_rate}.png', bbox_inches='tight', dpi=1600)
        plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse hybrid parallelism benchmark results')
    parser.add_argument('--file_path', type=str, help='Path to the benchmark log file')
    args = parser.parse_args()
    
    parse_benchmark_results(args.file_path)