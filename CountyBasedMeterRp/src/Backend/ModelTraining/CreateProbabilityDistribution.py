import os
from collections import defaultdict
import PasswordDetailsUtils
import json
from pathlib import Path

def save_distribution(data: dict, file_name: str, path: str):
    """
        Saves the dictionary in the provided path with the provided name

        Args:
            data: A dictionary of {key: p} pairs where Sum(dict.keys()) == 1
            file_name: The desiered name to the file created
            path: The path to the file created
    """
    distribution_path = "distribution"
    result_dir_path = path + "\\" + distribution_path
    Path(result_dir_path).mkdir(parents=True, exist_ok=True)
    file_name = result_dir_path + "\\" + file_name + ".json"
    with open(file_name, "w") as file :
        for key,value in data.items():
            file.write(f"{key} {value}\n")

def enrich_counts_from_files(file_path: str, base_word_count: defaultdict, prefix_count: defaultdict, suffix_count: defaultdict, shift_pattern_count: defaultdict, leet_pattern_count: defaultdict, ilegal_passwords: int):
    """
        Enriches the provided dictionaries according to the passowrds in the provided path
    """
    with open(file_path, "r") as read_file:
        array = json.load(read_file)
        for user in array:
            password = user['password']
            if not PasswordDetailsUtils.is_leagal_password(password):
                ilegal_passwords += 1
                continue
            [prefix, base_word, suffix] = PasswordDetailsUtils.parse_password_to_3d(password)
            if suffix_count != None:
                suffix_count[suffix] += 1
            if prefix_count != None:
                prefix_count[prefix] += 1
            if shift_pattern_count != None:
                shift_pattern = PasswordDetailsUtils.get_base_word_shift_pattern(base_word)
                if len(shift_pattern) == len(base_word):
                    shift_pattern_as_string = "all-cap"
                shift_pattern_as_string = str(shift_pattern)
                shift_pattern_count[shift_pattern_as_string] += 1
            if leet_pattern_count != None:
                (leet_pattern, base_word) = PasswordDetailsUtils.get_base_word_leet_pattern(base_word)
                leet_pattern_as_string = str(leet_pattern)
                leet_pattern_count[leet_pattern_as_string] += 1
            if base_word_count != None:
                base_word_count[base_word.lower()] += 1
    return ilegal_passwords

def count_to_distribution(count_dict: defaultdict):
    """
        Converts a dict of {key: count} to a distribution dict of {key: p} where p = count_dict[key] / sum(count_dict.values)

        Args:
            count_dict: A python dictionary of {key: count} pairs 

        Returns:
            A dictionary of {key: p} pairs where Sum(dict.keys()) == 1
    """
    if not count_dict == None:
        distribution_dict = {}
        total_size = sum(count_dict.values())
        for word in count_dict.keys():
            distribution_dict[word] = count_dict[word] / total_size
        sorted_distribution_dict = dict(sorted(distribution_dict.items()))
        return sorted_distribution_dict
    
def create_probability_disribution(path: str, get_prefix: bool, get_base_word: bool, get_suffix: bool, get_shift_pattern: bool, get_leet_pattern: bool):
    """
        Calculates the probability distribution of all the passwords under the provided path \n
        Args:
            path: Path of the passowrds
            get_prefix: If true, creates the prefix's probability distribution
            get_base_word: If true, creates the base-word's probability distribution
            get_suffix: If true, creates the suffix's probability distribution
            get_shift_pattern: If true, creates the shift pattern's probability distribution
    """
    prefix_count = defaultdict(int) if get_prefix else None
    base_word_count = defaultdict(int) if get_base_word else None
    suffix_count = defaultdict(int) if get_suffix else None
    shift_pattern_count = defaultdict(int) if get_shift_pattern else None
    leet_pattern_count = defaultdict(int) if get_leet_pattern else None
    ilegal_passwords = 0
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            ilegal_passwords = enrich_counts_from_files(file_path, base_word_count, prefix_count, suffix_count, shift_pattern_count, leet_pattern_count, ilegal_passwords)
    prefix_distribution_dict = count_to_distribution(prefix_count)
    base_word_distribution_dict = count_to_distribution(base_word_count)
    suffix_distribution_dict = count_to_distribution(suffix_count)
    shift_pattern_distribution_dict = count_to_distribution(shift_pattern_count)
    leet_pattern_distribution_dict = count_to_distribution(leet_pattern_count)
    save_distribution(prefix_distribution_dict, "a1", path)
    save_distribution(base_word_distribution_dict, "a2", path)
    save_distribution(suffix_distribution_dict, "a3", path)
    save_distribution(shift_pattern_distribution_dict, "a4", path)
    save_distribution(leet_pattern_distribution_dict, "a5", path)
    print(f"Ilegal passwords: {ilegal_passwords}")