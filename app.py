import flask
from flask import Flask 
from flask import render_template 
from flask import request
import json
import hashlib
import base64
from datetime import datetime
import os
import binascii
from flask import redirect

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

@app.route('/newpost', methods=['GET', 'POST'])
def post_page():
    if request.method == "POST":
        postdata = request.form["postdata"]
        postmaker = "A Lightbringer."
        if not postdata:
            return """
                <body style="background-color: black;">
                    <div style="color: red;">
                        <p style="text-align: center; font-size: large;">Missing Text To Post.</p>
                    </div>                
                </body>
            """
        with open('database/posts.json', 'r') as f:
            json_data = json.load(f)
        postdat_dict = {
            "postdata64": base64.b64encode(bytes(str(postdata), 'utf-8')).decode(),
            "timestamp": str(datetime.now()),
            "post_creator": postmaker,
            "post_randomizer_bytes": binascii.hexlify(os.urandom(50)).decode()
        }
        posthash = str(hashlib.md5(bytes(str(postdat_dict), 'utf-8')).hexdigest())
        json_data[posthash] = postdat_dict
        with open('database/posts.json', 'w+') as f:
            json.dump(json_data, f, indent=4)
        return redirect(f'/post/{posthash}')
    else:
        return render_template('newpost.html')


@app.route('/post/<postid>', methods=['GET'])
def post_by_id(postid):
    with open('database/posts.json', 'r') as f:
        json_data = json.load(f)
    if postid in json_data:
        post_data = json_data[postid]
    if postid not in json_data:
        return render_template('404.html')
    post_text = base64.b64decode(post_data["postdata64"].encode())
    return render_template('postbyid.html', post_data=post_data, text=str(post_text.decode()), post_id=postid)

@app.route('/post/search', methods=['GET', 'POST'])
def post_search():
    if request.method == "POST":
        postid = request.form.get("postid")
        return redirect(f'/post/{postid}')
    else:
        return render_template('search_post.html')
