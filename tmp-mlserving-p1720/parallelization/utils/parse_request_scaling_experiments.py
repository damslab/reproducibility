import re
import argparse
import matplotlib.pyplot as plt


def parse_benchmark_results(file_path):
    # Regular expressions to match parallelism type and benchmark results
    parallelism_pattern = re.compile(r'Running request rate scaling experiments for (.+)')
    request_rate_pattern = re.compile(r'Running with request rate: (\d+)')
    mean_ttft_pattern = re.compile(r'Mean TTFT \(ms\):\s+(\d+\.\d+)')
    token_throughput_pattern = re.compile(r'Output token throughput \(tok/s\):\s+(\d+\.\d+)')

    # Data storage
    results = {}

    # Read and parse log file
    with open(file_path, 'r') as f:
        current_parallelism = None
        current_request_rate = None
        for line in f:
            parallelism_match = parallelism_pattern.search(line)
            if parallelism_match:
                current_parallelism = parallelism_match.group(1)
                results[current_parallelism] = {'request_rate': [], 'mean_ttft': [], 'token_throughput': []}
                print(f"\nFound parallelism type: {current_parallelism}")
                continue
            
            request_rate_match = request_rate_pattern.search(line)
            if request_rate_match:
                current_request_rate = int(request_rate_match.group(1))
                print(f"\nRequest rate: {current_request_rate}")
                continue
            
            mean_ttft_match = mean_ttft_pattern.search(line)
            if mean_ttft_match and current_parallelism is not None and current_request_rate is not None:
                ttft = float(mean_ttft_match.group(1))
                results[current_parallelism]['request_rate'].append(current_request_rate)
                results[current_parallelism]['mean_ttft'].append(ttft)
                print(f"Mean TTFT: {ttft:.2f} ms")
                continue
            
            token_throughput_match = token_throughput_pattern.search(line)
            if token_throughput_match and current_parallelism is not None and current_request_rate is not None:
                throughput = float(token_throughput_match.group(1))
                results[current_parallelism]['token_throughput'].append(throughput)
                print(f"Token throughput: {throughput:.2f} tok/s")
                continue

    # Plot Mean TTFT vs Request Rate
    plt.figure(figsize=(10, 5))
    for parallelism, data in results.items():
        plt.plot(data['request_rate'], data['mean_ttft'], marker='o', linestyle='-', label=parallelism)
    plt.xlabel('Request Rate')
    plt.ylabel('Latency (ms)')
    plt.title('Latency vs Request Rate')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f'request_rate_scaling_latency.png', bbox_inches='tight', dpi=1600)
    plt.close()

    # Plot Token Throughput vs Request Rate
    plt.figure(figsize=(10, 5))
    for parallelism, data in results.items():
        plt.plot(data['request_rate'], data['token_throughput'], marker='o', linestyle='-', label=parallelism)
    plt.xlabel('Request Rate')
    plt.ylabel('Throughput (Tokens)')
    plt.title('Throughput vs Request Rate')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f'request_rate_scaling_throughput.png', bbox_inches='tight', dpi=1600)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse request rate scaling benchmark results')
    parser.add_argument('--file_path', type=str, help='Path to the benchmark log file')
    args = parser.parse_args()
    
    parse_benchmark_results(args.file_path)
