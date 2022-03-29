import flask
from flask import Flask 
from flask import render_template 
from flask import send_file
from flask import send_from_directory
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')

@app.route('/purpose', methods=['GET'])
def purpose_page():
    return render_template('purpose.html')
    
app.run(host='0.0.0.0', port=8080, debug=True)