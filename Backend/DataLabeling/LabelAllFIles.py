import os
import sys
from collections import defaultdict
from SaveJsonArrayTofile import save_json_array_to_file # Source: https://github.com/john-kurkowski/tldextract
from LabelEmailsUsingDomain import create_origin_label_wo_commercial, aggregate_meta_data_from_labeled_data, aggregate_meta_data_from_meta_data, enrich_country_dict

def label_all_files_in_path(path: str, domains_count, json_array: list):
    if os.path.isfile(path):
        try:
            curr_json = create_origin_label_wo_commercial(path, domains_count)
            save_json_array_to_file(curr_json, path.replace("\\", "/") + "_labeled_data.json")
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


def calculate_meta_data_by_directory(path: str, domains_count):
    if os.path.isfile(path) and path.find("labeled_data") > 0:
        aggregate_meta_data_from_labeled_data(path.replace("\\", "/"), domains_count)
    elif os.path.isdir(path):
        for root, directories, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                calculate_meta_data_by_directory(file_path, domains_count)
        save_json_array_to_file(domains_count, path.replace("\\", "/") + "/dir_meta_data.json")


def aggreagte_meta_data_from_meta_data_files(path: str, domains_count):
    if os.path.isfile(path) and path.find("meta_data") > 0:
        aggregate_meta_data_from_meta_data(path.replace("\\", "/"), domains_count)
    elif os.path.isdir(path):
        for root, directories, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                aggreagte_meta_data_from_meta_data_files(file_path, domains_count)
        save_json_array_to_file(domains_count, path.replace("\\", "/") + "/dir_meta_data.json")

def create_country_files(destination_path: str, path: str, country: str, country_data: list, file_index: int):
    if not os.path.exists(destination_path + "" f"/{country}"):
        os.makedirs(destination_path + "" f"/{country}")
    MAX_FILE_ENTRIES = 50000
    if os.path.isfile(path) and path.find("labeled_data") > 0:
        (country_data, file_index) = enrich_country_dict(destination_path, path, country, country_data, MAX_FILE_ENTRIES, file_index)
        return (country_data, file_index)
    elif os.path.isdir(path):
        for root, directories, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                (country_data, file_index) = create_country_files(destination_path=destination_path, path=file_path, country=country, country_data=country_data, file_index=file_index)
        return (country_data, file_index)
    return (country_data, file_index)
    
    
def main():
    path = sys.argv[1].replace("\\", "/")
    function = sys.argv[2]
    domains_count = defaultdict(int)
    if function == "label":
        json_array = []
        label_all_files_in_path(path, domains_count, json_array)
        save_json_array_to_file(domains_count, path + "/meta_data.json")
    elif function == "meta_data":
        calculate_meta_data_by_directory(path, domains_count=domains_count)
    elif function == "aggregate":
        aggreagte_meta_data_from_meta_data_files(path, domains_count)
    elif function == "country":
        country_data = []
        destination_path = sys.argv[3].replace("\\", "/")
        country = sys.argv[4]
        create_country_files(destination_path=destination_path, path=path, country=country, country_data=country_data, file_index=0)

if __name__ == "__main__":
    main()