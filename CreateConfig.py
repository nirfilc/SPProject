import os
import sys
import ESrank

def main():
    base_path = sys.argv[1]
    d = int(sys.argv[2])
    gamma = float(sys.argv[3])
    b = int(sys.argv[4])
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

if __name__ == "__main__":
    main()