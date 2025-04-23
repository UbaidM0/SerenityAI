from flask import Flask, jsonify, request
from flask_cors import CORS
from main import ai_api

app = Flask(__name__, template_folder='templates')

@app.route('/api', methods=['POST'])
#takes in input from the front end and puts it through the Ollama model
def handle_post():
        data = request.json
        message = str(data['message'])
        ans = ai_api(message)
        # Process the message here
        response = {
            'replies': ans
        }
        return jsonify(response)


CORS(app)
if __name__ == '__main__':
        app.run(port=5555, debug=True)
