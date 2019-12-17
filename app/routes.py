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
	# just for debugging now
	return render_template('list.html', newBooks=displayItems, oldBooks=displayItems)

@app.route('/add')
def add_recs():
	booksToList = AddRecs.testAdd()
	addedBooks = booksToList[0]
	existingBooks = booksToList[1]
	return render_template('list.html', newBooks=addedBooks, oldBooks=existingBooks)