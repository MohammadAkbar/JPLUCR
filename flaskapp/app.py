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
])

from flask_dance.contrib.google import make_google_blueprint, google
app.secret_key = "supersekrit"  # Replace this with your own secret!

blueprint = make_google_blueprint(
    client_id="1045884176358-7ujjr3afn72o8fpatg58gvtkbf48s9o7.apps.googleusercontent.com",
    client_secret="wxpbWHrKpva3SsPbeobgzLZK",
    scope=['email'],
    offline=True
)
app.register_blueprint(blueprint, url_prefix="/login")

testing = True

@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return render_template('dataVisual.html' , title='Data Visualization' , email=resp.json()["email"])
    #return resp.text

@app.route('/testing')
def testing():
    return render_template('dataVisual.html' , title='Data Visualization' , email='test@test.com')
    #return resp.text

@app.route('/savedata', methods = ['POST'])
def get_post_javascript_data():
	jsdata = str(request.form['javascript_data'])

	u = User.query.filter_by(email='test@test.com').first()
	if u is None:
		# if user does NOT have record , create new record
		newuser = User(email="test@test.com", data=jsdata)
		db.session.add(newuser)
		db.session.commit()
	else:
		# if user does have record , update record data
		u.data=jsdata
		db.session.commit()	
	return "sucess"

@app.route('/loaddata' , methods = ['POST'])
def load_map_data_string():
	jsdata = str(request.form['javascript_data'])
	u = User.query.filter_by(email=jsdata).first()
	print('user '+u.data, file=sys.stderr)
	return u.data
#def get_post_javascript_data():
#jsdata = str(request.form['javascript_data'])
#u = User(email="example@test.com", data="test")

#db.session.add(u)
#db.session.commit()
#print('postdata '+jsdata + ' \n stringtest: '+str(stringtest), file=sys.stderr)
#return "sucess"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,threaded=True,debug=True, ssl_context='adhoc')
    #app.run()
