import json
import multiprocessing
import os
import BS
import sys

def calculate_specific_country_tweaked_prob_factor(country, path, dimension, ratio):
    """
        To be calculated once offline.
        Sums the probabilities of the n most popular password of country in the general distribution = p_0.
        Then, sums the probability of these passwords in the country's specific distribution = p
        Returns the tweaking factor by this calculation: 1 - (p - p_0)
    """
    general_dist_path = os.path.join(path, dimension + ".txt")
    country_path = os.path.join(path, country, "distributions", f"{ratio}_{dimension}" + ".txt")
    is_4_or_5 = dimension in ["a4", "a5"]
    missing_passwords = []
    p_0, p = 0, 0
    with open(country_path, "r") as fp:
        str_line = fp.readline()
        while(str_line):
            line = str_line.split()
            last_space_index = str_line.rfind(" ")
            password = str_line[:last_space_index]
            if not is_4_or_5:
                for i in line[1:-1]:
                    password = password+" "+i
            word = password
            probability = line[-1]
            p += float(probability)
            general_p_str = BS.main4(general_dist_path, word) if is_4_or_5 else  BS.main(general_dist_path, word)
            p_0 += float(general_p_str) if general_p_str else 0
            if not general_dist_path:
                missing_passwords.append(word)
            str_line = fp.readline()
    res  = (p - p_0)
    print(country, dimension, res, missing_passwords)
    return 1 - res

def calculate_complete_tweaked_prob_factor(country, path, tweaking_factors, lock, ratio):
    dimensions = ["a1", "a2", "a3", "a4", "a5"]
    tweaking_factor = 1
    country_dict = {}
    for dimension in dimensions:
        dimension_tweaking_factor = calculate_specific_country_tweaked_prob_factor(country, path, dimension, ratio) 
        tweaking_factor *= dimension_tweaking_factor
        country_dict[dimension] = dimension_tweaking_factor
    country_dict["total"] = tweaking_factor
    with lock:
        tweaking_factors[country] = country_dict
    return tweaking_factor

def main():
    """
        A program that calculates async the tweaking factor for each country and each dimension and saves the final tweaking factors as a python dictionary.
        Usage: python CalculateFactor.py
    """
    ratios = [100, 200, 500, 1000]
    for ratio in ratios:
        tweaking_factors = multiprocessing.Manager().dict()
        lock = multiprocessing.Lock()
        processes = []
        countries = ["China", "France", "Germany", "Japan", "Poland", "United Kingdom (common practice)", "Italy", "India"]
        base_path = "C:\\School_data\\distributions"
        for country in countries:
            process = multiprocessing.Process(target=calculate_complete_tweaked_prob_factor, args=(country, base_path, tweaking_factors, lock, ratio))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
        with open(f"C:\\Users\\t-nirfilc\\OneDrive - Microsoft\\Desktop\\school_project\\SPProject\\tweakingFactors_{ratio}.py", "w+") as fp:
            real_dict = dict(tweaking_factors)
            json.dump(real_dict, fp)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()