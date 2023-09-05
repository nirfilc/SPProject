import math
from flask import Flask, request, jsonify
from flask_cors import CORS
import PESrank

app = Flask(__name__)
allowed_headers = ["Content-Type", "Authorization"]
allowed_methods = ["GET", "POST", "OPTIONS"] 

CORS(app, origins='*',
    allow_headers=allowed_headers,
    methods=allowed_methods)

@app.route('/api/getPasswordStrength', methods=['POST'])
def getPasswordStrength():
    print("got call")
    data = request.get_json()
    path = "/home/Distributions"
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required properties'}), 400

    username = data['username']
    password = data['password']
    country = data.get('country', '')
    try:
        res = PESrank.main(username, password, path, country)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500

    passwordStrength, explaination = prepareResult(res, country)
    return jsonify({'message': 'Data received successfully',
                    'username': username,
                    'strength': passwordStrength,
                    'reason': explaination 
                    })



def prepareResult(res, country):
    [rank, explain, isCountryDistribution] = res
    n = 905*(10**6)
    ex = False

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

    if isCountryDistribution:
        n = countiresSampleSize[country]

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

    if isCountryDistribution: 
        explaination = "According to this study, based on " + n + " leaked passwords from your country: \n"
    else:
        explaination = "According to this study, based on 905 million leaked passwords: \n"

    if ex == True:
        explaination += "Your password is based on the leaked word: '" +str(explain[0][1])+ "' that was used by",int(float(explain[0][2])*n), "people\n"
        for lst in explain[1:]:
            if math.ceil(float(lst[1])*n)>=100:
                if lst[0]==1:
                    explaination += "It uses a prefix that was used by",math.ceil(float(lst[1])*n), "people\n"
                if lst[0]==3:
                    explaination += "It uses a suffix that was used by",math.ceil(float(lst[1])*n), "people\n"
                if lst[0]==4:
                    explaination += "It uses a capitaliation pattern that was used by",math.ceil(float(lst[1])*n), "people\n"
                if lst[0]==5:
                    explaination += "It uses a l33t pattern that was used by",math.ceil(float(lst[1])*n), "people\n"
    
    return {"PasswordStrength": passwordStrength, "Explaination": explaination}


if __name__ == '__main__':
    app.run(debug=True)
