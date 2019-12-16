from app import app
from app.showRecords import ShowRecs
from app.addRecords import AddRecs
from flask import render_template

@app.route('/list')
def show_recs():
	displayStuff = ShowRecs.testShow()
	return render_template('index.html', books=displayStuff)

@app.route('/')
def add_recs():
	displayStuff = AddRecs.testAdd()
	return render_template('index.html', books=displayStuff)