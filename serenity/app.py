from flask import Flask, send_from_directory, render_template
import os

app = Flask(
    __name__,
    static_folder='TherapyAI/src',
    template_folder='TherapyAI'
)

@app.route('/')
def index():
    ''' Serve the React app '''
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_proxy(path):
    ''' Serve static files '''
    return send_from_directory(app.template_folder, path)

@app.route('/<path:path>')
def catch_all(path):
    ''' Serve the React app for any other route '''
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)