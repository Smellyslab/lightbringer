import flask
from flask import Flask 
from flask import render_template 

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', port=8080, debug=True)