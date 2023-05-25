import os
import json
from collections import defaultdict # Source: https://github.com/john-kurkowski/tldextract
from LabelEmailsUsingDomain import create_origin_label

def label_all_files_in_path(path, domains_count, json_array: list):
    if os.path.isfile(path):
        try:
            curr_json = create_origin_label(path, domains_count)
            return curr_json
        except:
            return []
    elif os.path.isdir(path):
        for root, directories, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                added_array = label_all_files_in_path(file_path, domains_count, json_array)
                json_array = json_array + added_array
    return json_array

def save_json_array_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def main(path):
    json_array = []
    domains_count = defaultdict(int)
    full_json = label_all_files_in_path(path, domains_count, json_array)
    meta_data_json = json.dumps(domains_count, indent=4)
    save_json_array_to_file(meta_data_json, path + "/meta_data.json")
    save_json_array_to_file(full_json, path + "/labeled_data.json")

path = "C:/Users/nirfi/Downloads/BreachCompilation/data/n"
main(path)