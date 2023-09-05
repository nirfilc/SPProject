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
        r, explain, isCountryDistribution = PESrank.main(username, password, path, country)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500


    return jsonify({'message': 'Data received successfully',
                    'username': username,
                    'result': (r, explain, isCountryDistribution)
                    })

if __name__ == '__main__':
    app.run(debug=True)
