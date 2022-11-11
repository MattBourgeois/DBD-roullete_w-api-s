from crypt import methods
from urllib import response
import requests, random
from flask import render_template, redirect, request, session, flash
from Flask_app import app
from Flask_app.models.user import Person
from datetime import date, timedelta
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/Reg')
def page():
	return render_template('Reg.html')


@app.route('/Register', methods = ['POST'])
def Register():
	data = {
		"first_name": request.form['first_name'],
		"last_name": request.form['last_name'],
		"email": request.form['email'],
		"password": bcrypt.generate_password_hash(request.form['password'])
	}
	id = Person.save(data)
	session['user_id'] = id
	return redirect('/dash')

@app.route('/login', methods = ['POST'])
def login():
	user = Person.get__by_email(request.form)
	if not user:
		flash ("Wrong Email", "login")
		return redirect('/')
	if not bcrypt.check_password_hash(user.password, request.form['password']):
		flash('Password incorrect', 'login')
		return redirect('/')
	session['user_id'] = user.id
	return redirect('/dash')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/dash')
def Dash():
	today = date.today()+timedelta(1)
	return render_template('dash.html', today = today)

@app.route('/acc')
def account():
	# user = Person.get_by_id()
	return render_template('account.html')


@app.route('/roll/killer')
def roll_killer():
    pass
    response = requests.get('https://dead-by-api.herokuapp.com/api/perks/killer')
    session['name'] = []
    for _ in range(4):
        a = response.json()['data'][random.randint(0, len(response.json()['data']) - 1)]['name']
        # if a != a:
        session['name'].append(a)
    print(session['name'])
    return redirect('/dash' )

@app.route('/roll')
def roller():
    response = requests.get('https://dead-by-api.herokuapp.com/api/perks/surv')
    session['perks'] = []
    for _ in range(4):
        a = response.json()['data'][random.randint(0, len(response.json()['data']) - 1)]['name']
    # if a != a:
        session['perks'].append(a)
    print(session['perks'])
    return redirect('/dash' )

@app.route('/reset')
def new():
    session.clear()
    return render_template('dash.html')