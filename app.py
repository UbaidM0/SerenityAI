from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from main import ai_api



app = Flask(__name__, template_folder='templates')

@app.route('/api', methods=['POST'])
def handle_post():
        data = request.json
        message = str(data['message'])
        ans = answer(message)
        # Process the message here
        response = {
            'replies': ans
        }
        print(response)
        return jsonify(response)

def answer(message):
        answer = ai_api(message)
        return answer



CORS(app)
if __name__ == '__main__':
        app.run(port=5555, debug=True)
