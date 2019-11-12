from __future__ import print_function
from flask import Flask, render_template, url_for, request, jsonify, redirect, Blueprint
from flask_navigation import Navigation
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import json
import os
import sys

app = Flask(__name__)

bootstrap = Bootstrap(app)

nav = Navigation(app)
nav.Bar('top',[
    nav.Item('Homepage', 'index'),
    nav.Item('Data Visualization', 'dataVisual'),
    nav.Item('Classify Data', 'dataClassify')
])

from flask_dance.contrib.google import make_google_blueprint, google
app.secret_key = "supersekrit"  # Replace this with your own secret!

blueprint = make_google_blueprint(
    client_id="1045884176358-7ujjr3afn72o8fpatg58gvtkbf48s9o7.apps.googleusercontent.com",
    client_secret="wxpbWHrKpva3SsPbeobgzLZK",
    scope=['https://www.googleapis.com/auth/userinfo.email'],
    offline=True
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return resp.text

@app.route('/dataVisual')
def dataVisual():
    return render_template('dataVisual.html' , title='Data Visualization')
    
@app.route('/dataClassify')
def dataClassify():
    return render_template('dataClassify.html', title='Data Classify')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,threaded=True,debug=False, ssl_context='adhoc')
    #app.run()
