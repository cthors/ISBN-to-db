from app import app
from app.showRecords import ShowRecs
from app.addRecords import AddRecs
from flask import render_template

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/list')
def show_recs():
	displayItems = ShowRecs.testShow()
	return render_template('list.html', records=displayItems)

@app.route('/add')
def add_recs():
	booksToList = AddRecs.testAdd()
	addedBooks = booksToList[0]
	existingBooks = booksToList[1]
	nonexistingBooks = booksToList[2]
	return render_template('list_added.html', newBooks=addedBooks, oldBooks=existingBooks, noBooks=nonexistingBooks)