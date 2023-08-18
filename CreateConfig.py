import os
import ESrank
d = 5
gamma = 1.09
b = 800
base_path = "C:\\Users\\nirfi\\Desktop\\data_by_country\\Italy\\distribution"
base_path = "C:\\Users\\nirfi\\Desktop\\text_files"
base_path = "C:\\Users\\nirfi\\Downloads\\BreachCompilation\\data"
P = []
for i in range(1, d + 1):
    path = os.path.join(base_path, "a" + str(i) + ".txt")
    with open(path, 'r') as f:
        file = f.read().splitlines()
        just_p = [float(line.split()[-1]) for line in file]
        P.append(just_p)
L1, L2 = ESrank.main1(P, d, gamma, b)

dest_path = os.path.join(base_path, "config.py")
with open(dest_path, 'w+') as f:
    f.write(f'L1 = {L1}\n')
    f.write(f'L2 = {L2}\n')