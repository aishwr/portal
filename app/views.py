from flask import render_template
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response,flash
from flask import session
from app.models import Login
from app import app, db
import pandas as pd
from passlib.hash import sha256_crypt
import datetime
import json

app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'


@app.route('/index')
@app.route('/')
def index():
	if 'username' in session:
		return render_template('home.html')
	else:
		return render_template('login.html')


def init_json():
	date_list = [datetime.datetime(2019, 6, 30) - datetime.timedelta(days=x) for x in range(540)]
	for item in range(len(date_list)):
		date_list[item] = date_list[item].date()
	dic = {}
	for i in date_list:
		dic[str(i)] = [[[0 for _ in range(4)] for _ in range(4)], 0]
	json_data = json.dumps(dic)
	return json_data

@app.route('/cancel')
def cancel():
	return render_template('cancel.html')

@app.route('/change')
def change():
	return render_template('change.html')


@app.route('/register')
def register():
	return render_template('login.html')


@app.route('/registerNext', methods=['GET', 'POST'])
def registerNext():
	try:
		user = Login(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"], rollNo=request.form["rollNo"], password=request.form['loginpassword'], json=init_json())
		db.session.add(user)
		db.session.commit()
	except:
		return "Email Id or Roll No already exists. Please check again."
	return redirect(url_for('home'))

@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/loginNext',methods=['GET','POST'])
def loginNext():

	if request.method == "POST":
		rollNo = request.form['LrollNo']
		password = request.form['Lloginpassword']

		user = Login.query.filter(and_(Login.rollNo == rollNo, Login.password == password)).first()
		if user:
			session['username'] = user.firstname
			return redirect(url_for('home'))
		return "Password Error"

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        name = session.pop('username')
        return render_template('login.html')


@app.route('/home.html')
@app.route('/home')
def home():
	if 'username' in session :
		return render_template('home.html')
	else:
		return render_template('login.html')
