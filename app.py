from flask import Flask, request, jsonify
import PESrank

app = Flask(__name__)

@app.route('/api/getPasswordStrength', methods=['POST'])
def getPasswordStrength():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required properties'}), 400

    username = data['username']
    password = data['password']
    country = data.get('country', '')

    res = PESrank.main(username, password, "C:\\Users\\nirfi\\Desktop\\text_files", country)


    return jsonify({'message': 'Data received successfully',
                    'username': username,
                    'result': res
                    })

if __name__ == '__main__':
    app.run(debug=True)
