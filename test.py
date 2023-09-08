import math
import PESrank

res = PESrank.main("goni", "123pa$$word!", "C:\\School_data\\distributions", "France")
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
mockresult1 = [281854.0, [(2, 'sakura', '5.203527357680634e-05'), (3, '0.0035326553265269327')], False]
mockresult2 = [2854311542.0, [(2, 'password', '0.0038755567716215905'), (1, '0.0016193523634648063'), (3, '0.0035326553265269327'), (5, ' 0.0006114594777399112\n')], True]
print("Your password is ",end="")
if rank<0:
    print("strong")
else:
    if math.log2(rank)<=30:
        print("weak", end="")
        ex=True
    elif math.log2(rank)<=50:
        print("sub-optimal", end="")
        ex=True
    else:
        print("strong", end="")

    print(", according to this study, based on 905 million leaked passwords")
        
if ex==True:
    print("Your password is based on the leaked word: '"+str(explain[0][1])+ "' that was used by",int(float(explain[0][2])*n), "people")
    for lst in explain[1:]:
        if math.ceil(float(lst[1])*n)>=100:
            if lst[0]==1:
                print("It uses a prefix that was used by",math.ceil(float(lst[1])*n), "people")
            if lst[0]==3:
                print("It uses a suffix that was used by",math.ceil(float(lst[1])*n), "people")
            if lst[0]==4:
                print("It uses a capitaliation pattern that was used by",math.ceil(float(lst[1])*n), "people")
            if lst[0]==5:
                print("It uses a l33t pattern that was used by",math.ceil(float(lst[1])*n), "people")

