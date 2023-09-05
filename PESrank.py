import os
import math
import time
import uuid
import ESrank
import BS
from pathlib import Path
import config_countries

import tweakingFactors_500
import tweakingFactors_100
import tweakingFactors_200
import tweakingFactors_1000

def keyBoard(word):
    for w in word:
        if not (w.isdigit() or w.isalpha() or isSymbol(w)):
            return False
    return True


def isSymbol(c):
    return (c in r"!~@#$%^&*()_+?><.,;:'{}[]=-|\/ ") or (c == '"')


def isShifted(c):
    if c.isalpha():
        return c.isupper()
    return False


def unShiftLetter(c):
    if c.isalpha():
        return c.lower()


def unShiftWord(word):
    p = ""
    lst = []
    for i in range(len(word)):
        if isShifted(word[i]):
            p = p+unShiftLetter(word[i])
            if i > len(word)//2:
                lst.append(i-len(word))
            else:
                lst.append(i)
        else:
            p = p+word[i]
    return p, str(lst)


def isascii(value):
    return all(ord(c) < 128 for c in value)


def unLeetWord(word):
    lst = []
    if "0" in word:
        word = word.replace("0", "o")
        lst.append(1)
    if "1" in word:
        word = word.replace("1", "i")
        lst.append(12)
    elif "!" in word:
        word = word.replace("!", "i")
        lst.append(13)
    if "@" in word:
        word = word.replace("@", "a")
        lst.append(2)
    elif "4" in word:
        word = word.replace("4", "a")
        lst.append(3)
    if "3" in word:
        word = word.replace("3", "e")
        lst.append(6)
    if "$" in word:
        word = word.replace("$", "s")
        lst.append(4)
    elif "5" in word:
        word = word.replace("5", "s")
        lst.append(5)
    if "2" in word:
        word = word.replace("2", "z")
        lst.append(11)
    if "%" in word:
        word = word.replace("%", "x")
        lst.append(14)
    if "7" in word:
        word = word.replace("7", "t")
        lst.append(10)
    elif "+" in word:
        word = word.replace("+", "t")
        lst.append(9)
    if "9" in word:
        word = word.replace("9", "g")
        lst.append(8)
    elif "6" in word:
        word = word.replace("6", "g")
        lst.append(7)
    return word, str(tuple(sorted(lst)))

def get_tweaking_factor(country, ratio):
    if ratio == 500:
        return tweakingFactors_500.tweakingFactor[country]["total"]
    elif ratio == 100:
        return tweakingFactors_100.tweakingFactor[country]["total"]
    elif ratio == 200:
        return tweakingFactors_200.tweakingFactor[country]["total"]
    elif ratio == 1000:
        return tweakingFactors_1000.tweakingFactor[country]["total"]


def main(username, password, path, country="", ratio=500): 
    if country in ["China", "France", "Germany", "Japan", "Poland", "United Kingdom (common practice)", "Italy", "India"]:
        r,explain = get_country_rank(password, country, path, ratio)
        isCountryDistribution = True
        # If the password isn't among the 10,000 country's most popular passwords
        if r == -5:
            tweaked_prob_factor = get_tweaking_factor(country, ratio)
            r,explain = rank(password, path, "", tweaked_prob_factor)
            isCountryDistribution = False
    else:
        r, explain = rank(password, path, "")
        isCountryDistribution = False
    y = str(uuid.uuid1())
    dir_path = os.path.join(path, "out")
    file_path = os.path.join(dir_path, str(y) + ".txt")
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with open(file_path, "w+") as f:
        try:
            f.write(
                ",".join([username,  str(math.log2(r)) if r > 0 else "strong!", str(time.asctime())]) + "\n")
        except Exception as e:
            f.write(f"Can't save username, {e}" "\n")
    return r, explain, isCountryDistribution

def get_country_rank(password, country, path, ratio):
    path = os.path.join(path, country)
    return rank(password, path, country, 1, ratio)

def get_lists(country):
    if not country:
        country = "General"
    L1 = config_countries.config[country]["L1"]
    L2 = config_countries.config[country]["L2"]
    return L1, L2

def rank(password, path, country, tweaked_country_prob_factor=1, ratio=500):        
    a1_path = os.path.join(path, f"{ratio}_a1.txt" if country else "a1.txt")
    a2_path = os.path.join(path, f"{ratio}_a2.txt" if country else "a2.txt")
    a3_path = os.path.join(path, f"{ratio}_a3.txt" if country else "a3.txt")
    a4_path = os.path.join(path, f"{ratio}_a4.txt" if country else "a4.txt")
    a5_path = os.path.join(path, f"{ratio}_a5.txt" if country else "a5.txt")

    L = -5
    explain=[]
    first = True
    last = True
    f = len(password)
    l = -1
    if (isascii(password)):
        for i in range(len(password)):
            if (not (password[i].isdigit() or isSymbol(password[i]))) and (first == True):
                f = i
                first = False
            if (not (password[-(i+1)].isdigit() or isSymbol(password[-(i+1)]))) and (last == True):
                l = -(i+1)
                last = False
        if f == len(password):
            p = password[0:f]
            maxProb = 0
            for i in range(0, len(p)+1):
                for j in range(i, len(p)+1):
                    P1 = p[:i]
                    unLeetP2 = p[i:j]
                    P3 = p[j:]
                    probability1 = BS.main(a1_path, P1)
                    probability2 = BS.main(a2_path, unLeetP2)
                    probability3 = BS.main(a3_path, P3)

                    if (probability1 != None and probability2 != None and probability3 != None):
                        if float(probability1)*float(probability2)*float(probability3) > maxProb:
                            maxProb = float(probability1)*float(probability2)*float(probability3)
                            G1=P1
                            G2=unLeetP2
                            G3=P3
                            g1=probability1
                            g2=probability2
                            g3=probability3
                            

            pos1 = "[]"
            pos2 = "()"
            if maxProb > 0:
                probability4 = BS.main4(a4_path, pos1)
                probability5 = BS.main4(a5_path, pos2)
                if (probability1 != None and probability2 != None and probability3 != None and probability4 != None and probability5 != None):
                    prob = maxProb*float(probability4)*float(probability5)*tweaked_country_prob_factor
                    L1, L2 = get_lists(country)
                    L = ESrank.main2(L1, L2, prob, 14)
                    L = sum(L)/2
                    
                    explain=[]
                    if G2!="":
                        explain.append([2,G2,g2])
                    if G1!="":
                        explain.append([1,g1])
                    if G3!="":
                        explain.append([3,g3])
                else:
                    L = -5
                    explain=[]
            else:
                L = -5
                explain=[]
        else:
            if f != 0:
                P1 = password[0:f]
                if l != -1:
                    P2 = password[f:l+1]
                    P3 = password[l+1:]
                else:
                    P2 = password[f:]
                    P3 = ""
            else:
                P1 = ""
                if l != -1:
                    P2 = password[f:l+1]
                    P3 = password[l+1:]
                else:
                    P2 = password[f:]
                    P3 = ""

            unShiftP2, pos1 = unShiftWord(P2)
            unLeetP2, pos2 = unLeetWord(unShiftP2)
            probability1 = BS.main(a1_path, P1)
            probability2 = BS.main(a2_path, unLeetP2)
            probability3 = BS.main(a3_path, P3)
            if country== "China" and pos1 == "[]":
                print("this")
            probability4 = BS.main4(a4_path, pos1)
            probability5 = BS.main4(a5_path, pos2)

            # TODO We should return independet info about each part so that if one part is weak we'll infrom the user even if other parts where not found and are None
            if (probability1 != None and probability2 != None and probability3 != None and probability4 != None and probability5 != None):
                prob = float(probability1)*float(probability2)*float(probability3)*float(probability4)*float(probability5)*tweaked_country_prob_factor
                L1, L2 = get_lists(country)
                L = ESrank.main2(L1, L2, prob, 14)
                L = sum(L)/2
                
                explain=[]
                if unLeetP2!="":
                    explain.append((2,unLeetP2,probability2))
                if P1!="":
                    explain.append((1,probability1))
                if P3!="":
                    explain.append((3,probability3))
                if pos1!="[]":
                    explain.append((4,probability4))
                if pos2!="()":
                    explain.append((5,probability5))
                
            else:
                L = -5
                explain=[]
                

    return [L,explain]
