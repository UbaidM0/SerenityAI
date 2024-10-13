from flask import Flask, render_template
from requests import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template()
    if request.method == 'POST':
        return

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)