import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_cdf(data):
    """
    Plots the CDF of the number of attempts until success for each ratio.
    """
    fig = plt.figure()
    plt.figure(figsize=(8, 6))
    plt.xlabel('Number of Attempts')
    plt.ylabel('Cumulative Percentage of Items')
    plt.title('CDF Curve of Number of Attempts Until Success')
    plt.grid(True)
    plt.ylim(0, 1.1)
    max_x_value = 0
    plt.xscale('log')  # Set x-axis to logarithmic scale
#     plt.yscale('log')
    for label, attempts_dict in data.items():
     total_items = sum(attempts_dict.values())
     x_str_values = sorted(attempts_dict.keys())
     x_values = [float(item) for item in x_str_values]
     y_values = [sum(attempts_dict[str(x_prime)] for x_prime in x_values if x_prime <= x) / total_items for x in x_values]
     max_x_value = max(max_x_value, max(x_values))
     plt.plot(x_values, y_values, marker='s', markersize=72./fig.dpi, linestyle = 'None', label=f'{label}')
#     plt.xticks(range(1, int(max_x_value) + 1))

    plt.legend(loc='lower right', markerscale=12)
#     plt.xlim(0, int(max_x_value) + 1)
    plt.yticks([i/10 for i in range(11)])
    
    plt.show()
    plt.savefig("cdf_plot_new.pdf", format='pdf', bbox_inches='tight')
    plt.close()