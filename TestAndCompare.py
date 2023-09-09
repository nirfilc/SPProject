import PESrank
import json
import os
import multiprocessing
import sys
import plot_cdf

folder_path = "C:\\Test_data\\IN_USE"
model_path = "C:\\School_data\\distributions"

countries_list = ["China", "France", "Germany", "Japan", "Poland", "United Kingdom (common practice)", "Italy", "India"]

def test_file(file_path, ratio, cdf, cdf_improved, general_data, lock):
     with open(file_path, 'r') as file:
          content = json.load(file)
          for entry in content:
               email = entry['email']
               password = entry['password'][:-1]
               country = entry['country']
               if country not in countries_list:
                    continue
               res1 = PESrank.main(email, password, model_path)
               res2 = PESrank.main(email, password, model_path, country, ratio)

               [rank_1, _, _] = res1
               [rank_2, _, _] = res2
               if rank_1 != -5 and rank_2 != -5:
                    with lock:
                         cdf[rank_1] = cdf.get(rank_1, 0) + 1
                         cdf_improved[rank_2] = cdf_improved.get(rank_2, 0) + 1
                         if country in general_data:
                              values_dict = general_data.get(country)
                              values_dict['entries'] = values_dict.get('entries') + 1
                              values_dict['sum_rank_original'] = values_dict.get('sum_rank_original') + rank_1
                              values_dict['sum_rank_improved'] = values_dict.get('sum_rank_improved') + rank_2 
                              general_data[country] = values_dict
                              
                         else:
                              values_dict = {'entries': 1, 'sum_rank_original': rank_1, 'sum_rank_improved': rank_2}
                              general_data[country] = values_dict

def Test():
     top_countries_data = {}
     general_data = multiprocessing.Manager().dict()
     lock = multiprocessing.Lock()
     ratios = [100, 200, 500, 1000]
     cdfs = {}
     for ratio in ratios:
          cdf = multiprocessing.Manager().dict()
          cdf_improved = multiprocessing.Manager().dict()
          for root, dirs, files in os.walk(folder_path):
               processes = []
               for file_name in files:
                    file_path = os.path.join(root, file_name)
                    process = multiprocessing.Process(target=test_file, args=(file_path, ratio, cdf, cdf_improved, general_data, lock))
                    processes.append(process)
                    process.start()
               for process in processes:
                    process.join()

          for country in general_data:
               values_dict = general_data.get(country)
               org_rank = values_dict.get('sum_rank_original')
               imp_rank = values_dict.get('sum_rank_improved')
               entries = values_dict.get('entries')
               values_dict['avg_rank_origianl'] = org_rank / entries
               values_dict['avg_rank_original'] = imp_rank / entries
               values_dict['diff'] = (imp_rank / entries) - (org_rank / entries)

               general_data[country] = values_dict

               if country in countries_list:
                    top_countries_data[country] = values_dict


          with open(f'test_output_general_{ratio}_new.json', 'w+') as file:
               json.dump(dict(general_data), file, indent=4)

          with open(f'test_output_countries_{ratio}_new.json', 'w+') as file:
               json.dump(top_countries_data, file, indent=4)
          cdfs[ratio] = dict(cdf_improved)
     cdfs["General"]= dict(cdf)
     with open(f'test_output_cdfs.json', 'w+') as file:
          json.dump(cdfs, file, indent=4)

def get_weighted_diff(data):
     file_data = {}
     weighted_diff = 0
     total_entries = 0
     number_of_improved_countries = 0
     for country in data:
          values_dict = data.get(country)
          entries = values_dict.get('entries')
          diff = values_dict.get('diff')
          total_entries += entries
          weighted_diff += diff * entries
          if diff < 0:
               number_of_improved_countries += 1
     file_data["weighted_diff"] = weighted_diff / total_entries
     file_data["number_of_improved_countries"] = number_of_improved_countries
     return file_data

def Compare():
     ratios = [100, 200, 500, 1000]
     weighted_diffs = {}
     for ratio in ratios:
          with open(f'test_output_countries_{ratio}_new.json', 'r') as file:
               data = json.load(file)
               weighted_diffs[ratio] = get_weighted_diff(data)

     with open(f'Compare_ratios_new.json', 'w+') as file:
          json.dump(weighted_diffs, file, indent=4)
     
     with open(f'test_output_cdfs.json', 'r') as file:
          data = json.load(file)
          plot_cdf(data)

def main():
     action = sys.argv[1]
     if action == 'test':
          Test()
     elif action == 'compare':
          Compare()
                
if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

ratios = [100, 200, 500, 1000]

# for country in countries_list:
#      country_data = {}
#      for ratio in ratios:
#           with open(f'test_output_countries_{ratio}_new.json', 'r') as file:
#                data = json.load(file)
#                country_data[ratio] = data.get(country).get('diff')
#      print(country)
#      sorted_by_value = sorted(country_data.items(), key=lambda kv: kv[1])
#      print(sorted_by_value)