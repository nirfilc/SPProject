import json
import os
import tweakingFactors_100
import tweakingFactors_200
import tweakingFactors_500
import tweakingFactors_1000

"""
    Utilitis for creating latex tables.
"""

with open("test_output_general_500_a_and_numbers.json", "r") as f:
    data = json.load(f)

    for country in data:
        values_dict = data.get(country)
        org_rank = values_dict.get('sum_rank_original')
        imp_rank = values_dict.get('sum_rank_improved')
        entries = values_dict.get('entries')
        values_dict['avg_rank_origianl'] = org_rank / entries
        values_dict['avg_rank_original'] = imp_rank / entries
        values_dict['diff'] = (imp_rank / entries) - (org_rank / entries)

entries = "entries"
with open("test_output_countries_1000_1.json", "w+") as f1:
    with open("test_output_countries_1000.json", "r") as f2:
        data2 = json.load(f2)
    json.dump(data2, f1, indent=4, sort_keys=True)

for country in ["China", "France", "Germany", "Japan", "Poland", "United Kingdom (common practice)", "Italy", "India"]:
    t1000 = tweakingFactors_1000.tweakingFactor[country]['total']
    t500 = tweakingFactors_500.tweakingFactor[country]['total']
    t200 = tweakingFactors_200.tweakingFactor[country]['total']
    t100 = tweakingFactors_100.tweakingFactor[country]['total']
    print(f"{country} & {round(t100,3)} & {round(t200,3)} & {round(t500,3)} & {round(t1000,3)} \\\\")
    print("\\hline")

for country in ["China", "France", "Germany", "Japan", "Poland", "United Kingdom (common practice)", "Italy", "India"]:
    path = os.path.join("C:\School_data\distributions", country, "model_size.txt")
    with open(path, "r") as f:
        line = f.readline().split()
        print(f"{country} & {line[-1]} \\\\")
        print("\\hline")
