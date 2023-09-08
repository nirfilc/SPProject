import os
import sys
from CreateConfig import save_sorted_p
import ESrank
import multiprocessing

def get_country_config(country, d, gamma, b, base_path, save_sorted, lock, configs):
    P = []
    for i in range(1, d + 1):
        path = os.path.join(base_path, country, "distributions")
        with open(os.path.join(path, "a" + str(i) + ".txt"), 'r') as f:
            file = f.read().splitlines()
            just_p = [float(line.split()[-1]) for line in file]
            just_p.sort(reverse=True)
            if save_sorted:
                save_sorted_p(just_p, i, path)
            P.append(just_p)
    L1, L2 = ESrank.main1(P, d, gamma, b)
    with lock:
        configs[country] = {"L1": L1, "L2": L2}

def main():
    """
        To be calculated once offline.
        Calculates async the L1 and L2 values for the ESrank algorithm for all the countries.

        Args:
            base_path: the path to the folder containing the distributions for all the countries.
            d: number of dimensions (used 5 for this project)
            gamma: the gamma value used in the ESrank algorithm (used 1.09 for this project)
            b: the b value used in the ESrank algorithm (used 14 for this project). Should be such taht (b + 1) / b < gamma.
            save_sorted: whether to save the sorted distributions or not. Good for debugging, to prevent the need to sort the distributions every time.
    """
    configs = multiprocessing.Manager().dict()
    lock = multiprocessing.Lock()
    base_path = sys.argv[1]
    d = int(sys.argv[2])
    gamma = float(sys.argv[3])
    b = int(sys.argv[4])
    save_sorted = bool(sys.argv[5])
    countries = ["China", "Poland", "United Kingdom (common practice)", "Italy", "India", "France", "Germany", "Japan"]
    processes = []
    for country in countries:
        process = multiprocessing.Process(target=get_country_config, args=(country, d, gamma, b, base_path, save_sorted, lock, configs))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    dest_path = os.path.join(base_path, "config_countries.py")
    with open(dest_path, 'w+') as f:
        f.write("config = " + str(configs))

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()