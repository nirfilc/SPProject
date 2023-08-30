import PESrank
import json
import os

folder_path = "/Users/skhatib/Downloads/test-data/"


countries_list = ['Russion Federation (the)', 'Germany', 'France', 'United Kingdom (common practice)', 'Italy', 'Poland', 'China', 'Japan']
general_data = {}
top_countries_data = {}

for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            with open(file_path, 'r') as file:
                 content = json.load(file)

            for entry in content:
                email = entry['email']
                password = entry['password']
                country = entry['country']

                res1 = PESrank.main(email, password, "/Users/skhatib/Downloads/PESrank")
                res2 = PESrank.main(email, password, "/Users/skhatib/Downloads/PESrank", country)

                [rank_1,explain_1] = res1
                [rank_2,explain_2] = res2

                if country in general_data:
                     values_dict = general_data.get(country)
                     values_dict['entries'] = values_dict.get('entries') + 1
                     values_dict['sum_rank_original'] = values_dict.get('sum_rank_original') + rank_1
                     values_dict['sum_rank_improved'] = values_dict.get('sum_rank_improved') + rank_2 
                     general_data[country] = values_dict
                     
                else:
                     values_dict = {'entries': 1, 'sum_rank_original': rank_1, 'sum_rank_improved': rank_2}
                     general_data[country] = values_dict

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


with open('test_output_general.json', 'w') as file:
     json.dump(general_data, file, indent=4)

with open('test_output_countries.json', 'w') as file:
     json.dump(top_countries_data, file, indent=4)
                
