import json
import os
import BS


def calculate_specific_country_tweaked_prob_factor(country, path, general_dist_path, dimension):
    """
        To be calcullated once offline.
        Sums the probabilities of the n most popular password of country in the general distribution = p_0.
        Then, sums the probability of these passwords in the country's specific distribution = p
        Returns the tweaking factor by this calculation: 1 - (p - p_0)
    """
    path = os.path.join(path, country, dimension + ".txt")
    general_dist_path = os.path.join(general_dist_path, dimension + ".txt")
    is_4_or_5 = dimension in ["a4", "a5"]
    missing_passwords = []
    p_0, p = 0, 0
    with open(path, "r") as fp:
        str_line = fp.readline()
        while(str_line):
            line = str_line.split()
            if len(line) == 1:
                word = ""
                probability = line[0]
            else:
                last_space_index = str_line.rfind(" ")
                password = str_line[:last_space_index]
                if not is_4_or_5:
                    for i in line[1:-1]:
                        password = password+" "+i
                word = password
                probability = line[-1]
            p += float(probability)
            if dimension == "a4":
                word = word.replace("[", "(").replace("]", ")")
            general_p_str = BS.main4(general_dist_path, word) if is_4_or_5 else  BS.main(general_dist_path, word)
            p_0 += float(general_p_str) if general_p_str else 0
            if not general_dist_path:
                missing_passwords.append(word)
            str_line = fp.readline()
    res  = (p - p_0)
    print(country, dimension, res, missing_passwords)
    return 1 - res

def calculate_complete_tweaked_prob_factor(country, path, general_dist_path):
    dimensions = ["a1", "a2", "a3", "a4", "a5"]
    tweaking_factors = {}
    tweaking_factor = 1
    for dimension in dimensions:
        dimension_tweaking_factor = calculate_specific_country_tweaked_prob_factor(country, path, general_dist_path, dimension) 
        tweaking_factor *= dimension_tweaking_factor
        tweaking_factors[dimension] = dimension_tweaking_factor
    tweaking_factors["total"] = tweaking_factor
    with open(os.path.join(path, country, "tweaking_factors.json"), "w+") as fp:
        json.dump(tweaking_factors, fp)
    return tweaking_factor

countries = ["China", "France", "Germany", "Japan", "Poland", "United Kingdom (common practice)", "Italy", "India"]
base_path = "C:\\Users\\nirfi\\Desktop\\data_by_country\\new_data"
for country in countries:
    # Cahnge the path to the correct one after I fix the text files I generate.
    tweaking = calculate_complete_tweaked_prob_factor(country, base_path, "C:\\Users\\nirfi\\Desktop\\text_files")
    print(tweaking)
