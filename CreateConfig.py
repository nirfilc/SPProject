import os
import sys
import ESrank

def save_sorted_p(p, i, path):
    path = os.path.join(path, "a" + str(i) + "_sorted.txt")
    with open(path, 'w+') as f:
        for item in p:
            f.write("%s\n" % item)

def main():
    base_path = "C:\\School_data\\distributions"
    d = int(sys.argv[2])
    gamma = float(sys.argv[3])
    b = int(sys.argv[4])
    save_sorted = bool(sys.argv[5])
    P = []
    for i in range(1, d + 1):
        path = os.path.join(base_path, "a" + str(i) + ".txt")
        with open(path, 'r') as f:
            file = f.read().splitlines()
            just_p = [float(line.split()[-1]) for line in file]
            just_p.sort(reverse=True)
            if save_sorted:
                save_sorted_p(just_p, i, base_path)
            P.append(just_p)
    L1, L2 = ESrank.main1(P, d, gamma, b)

    dest_path = os.path.join(base_path, "config2.py")
    with open(dest_path, 'w+') as f:
        f.write(f'L1 = {L1}\n')
        f.write(f'L2 = {L2}\n')

if __name__ == "__main__":
    main()