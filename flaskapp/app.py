from __future__ import print_function
from flask import Flask, render_template, url_for, request, jsonify, redirect, Blueprint
from flask_navigation import Navigation
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import json
import os
import sys
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy


os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	data = db.Column(db.String, unique=False, nullable=True)
	def __init__(self, email, data ):
		self.email = email
		self.data = data
db.create_all()
#users = User.query.all()
app.wsgi_app = ProxyFix(app.wsgi_app)

bootstrap = Bootstrap(app)

nav = Navigation(app)
nav.Bar('top',[
    nav.Item('Homepage', 'index'),
    nav.Item('View Data', 'viewData'),
    nav.Item('Classify Data' , 'classifyData')
])

from flask_dance.contrib.google import make_google_blueprint, google
app.secret_key = "supersekrit"  # Replace this with your own secret!

blueprint = make_google_blueprint(
    client_id="1045884176358-7ujjr3afn72o8fpatg58gvtkbf48s9o7.apps.googleusercontent.com",
    client_secret="wxpbWHrKpva3SsPbeobgzLZK",
	reprompt_consent=True,
    offline=True,
    scope=['email']
)
app.register_blueprint(blueprint, url_prefix="/login")

testing = True

@app.route('/')
def index():
	users = User.query.order_by(User.email).all()
	return render_template('dataVisual.html' , title='Data Visualization' , email="none", users=users)
    #return resp.text

@app.route('/testing')
def testing():
    return render_template('dataVisual.html' , title='Data Visualization' , email='test@test.com')
    #return resp.text

@app.route('/savedata', methods = ['POST'])
def get_post_javascript_data():
	jsdata = str(request.form['javascript_data'])
	email = str(request.form['email'])
	u = User.query.filter_by(email=email).first()
	if u is None:
		# if user does NOT have record , create new record
		newuser = User(email=email, data=jsdata)
		db.session.add(newuser)
		db.session.commit()
	else:
		# if user does have record , update record data
		u.data=jsdata
		db.session.commit()	
	return "sucess"

@app.route('/loaddata' , methods = ['POST'])
def load_map_data_string():
	email = str(request.form['email'])
	u = User.query.filter_by(email=email).first()
	return u.data

@app.route('/viewData')
def viewData():
	users = User.query.order_by(User.email).all()
	return render_template('dataVisual.html' , title='Data Visualization' , email="none", users=users)

@app.route('/classifyData')
def classifyData():
	if not google.authorized:
		return redirect(url_for("google.login"))
	resp = google.get("/oauth2/v2/userinfo")
	assert resp.ok, resp.text
	return render_template('dataClassify.html' , title='Data Classsification' , email=resp.json()["email"])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,threaded=True,debug=True, ssl_context='adhoc')
    #app.run()
