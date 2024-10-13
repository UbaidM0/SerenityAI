from flask import Flask
from main import main
app = Flask(__name__)

app.route('/input')
def input():
    return {'input': 'weiner'}