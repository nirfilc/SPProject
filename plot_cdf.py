import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_cdf(attempts_dict):
    total_items = sum(attempts_dict.values())
    x_values = sorted(attempts_dict.keys())
    y_values = [sum(attempts_dict[x_prime] for x_prime in x_values if x_prime <= x) / total_items for x in x_values]
    fig = plt.figure()
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, marker='s', markersize=72./fig.dpi, linestyle='None', label='CDF')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Cumulative Percentage of Items')
    plt.title('CDF Curve of Number of Attempts Until Success')
    plt.grid(True)
    plt.xlim(0, max(x_values) + 1)
    plt.ylim(0, 1)
    plt.xticks(range(1, max(x_values) + 1))
    plt.yticks([i/10 for i in range(11)])
    
    plt.legend(loc='lower right', markerscale=12)
    fig.tight_layout()
    plt.show()

# Example dictionary where key 'x' represents the number of successes
# and the value represents the number of items that needed 'x' attempts until success
attempts_dict = {
    1: 50,
    2: 30,
    3: 15,
    4: 5,
}

plot_cdf(attempts_dict)
