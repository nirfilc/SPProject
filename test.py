import math
import PESrank

res = PESrank.main("goni", "123pa$$word", "C:\\School_data\\distributions", "France")
[rank, explain, isCountryDistribution] = res
n=905*(10**6)
ex=False
countiresSampleSize = {
    "China": 6152365,
    "France": 33090150,
    "Germany": 47567442,
    "India": 2226505,
    "Italy": 17904278,
    "Japan": 4482526,
    "Poland": 9811562,
    "United Kingdom (common practice)": 18289350
}
mockresult1 = [281854.0, [(2, "sakura", "5.203527357680634e-05"), (3, '0.0035326553265269327')], False]
mockresult2 = [2854311542.0, [(2, 'password', '0.0038755567716215905'), (1, '0.0016193523634648063'), (3, '0.0035326553265269327'), (5, ' 0.0006114594777399112\n')], True]
res = mockresult1
[rank, explain, isCountryDistribution] = res
if isCountryDistribution:
        n = countiresSampleSize["France"]

passwordStrength = "" 
if rank<0:
    passwordStrength = "Strong"
else:
    if math.log2(rank)<=30:
        passwordStrength = "Weak"
        ex=True
    elif math.log2(rank)<=50:
        passwordStrength = "Sub-Optimal"
        ex=True
    else:
        passwordStrength = "Strong"
explaination = ""
if isCountryDistribution: 
    explaination += "According to this study, based on " + str(n) + " leaked passwords from your country: \n"
else:
    explaination += "According to this study, based on 905 million leaked passwords: \n"
if ex == True:
    explaination += "Your password is based on the leaked word: '" +str(explain[0][1])+ "' that was used by " + str(int(float(explain[0][2])*n)) + " people\n"
    for lst in explain[1:]:
        if math.ceil(float(lst[1])*n)>=100:
            if lst[0]==1:
                explaination += "It uses a prefix that was used by " + str(math.ceil(float(lst[1])*n)) + " people\n"
            if lst[0]==3:
                explaination += "It uses a suffix that was used by " + str(math.ceil(float(lst[1])*n)) + " people\n"
            if lst[0]==4:
                explaination += "It uses a capitaliation pattern that was used by " + str(math.ceil(float(lst[1])*n)) + " people\n"
            if lst[0]==5:
                explaination += "It uses a l33t pattern that was used by " + str(math.ceil(float(lst[1])*n)) + " people\n"

print(passwordStrength)
print(explaination)
