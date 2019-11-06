from __future__ import print_function
from flask import Flask, render_template, url_for, request, jsonify
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

@app.route('/')
def index():
    return render_template('dataVisual.html' , title='Homepage')

@app.route('/dataVisual')
def dataVisual():
    return render_template('dataVisual.html' , title='Data Visualization')
    
@app.route('/dataClassify')
def dataClassify():
    return render_template('dataClassify.html', title='Data Classify')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,threaded=True,debug=False, ssl_context=('cert.pem', 'key.pem'))
    #app.run()
