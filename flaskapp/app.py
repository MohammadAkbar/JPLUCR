from __future__ import print_function
from flask import Flask, render_template, url_for, request, jsonify
from flask_navigation import Navigation
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import json
import os

import sys

app = Flask(__name__)

# database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100),unique=True)
	data = db.Column(db.String())

	def __init__(self,username,data):
		self.username=username
		self.data=data
# user schema
class UserSchema(ma.Schema):
	class Meta:
		fields = ('id','username','data')

# init schema		
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True,strict=True)

@app.route('/load', methods=['GET','POST'])
def load():
	#nm = request.get_json()
	nm = str(request.json['username'])
	print(nm, file=sys.stderr)
	#new_user = User("username","data")
	userdata = User.query.filter_by(username=nm).first()
	print(userdata.data, file=sys.stderr)

	return jsonify(userdata.data)
	#db.session.add(new_user)
	#db.session.commit()
	#return user_schema.jsonify(new_user)

# Get user data
@app.route('/save',methods=['GET','POST'])
def save():
	#nm = str(request.json["username"])
	nm = "testuser"
	u = User.query.filter_by(username=nm).first()
	print(u.data, file=sys.stderr)
	if u is None:
		print("case1", file=sys.stderr)
		new_user = User(nm,"temp")
		db.session.add(new_user)
		db.session.commit()
		return jsonify(new_user.data)
	else:
		print(request.get_data(), file=sys.stderr)
		u.data = request.get_data()
		db.session.commit()
		return jsonify(u.data)

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
    app.run(host='0.0.0.0',port=80,threaded=True,debug=True)
    #app.run()
