from app import app
from app.showRecords import ShowRecs
from app.addRecords import AddRecs
from flask import render_template

@app.route('/list')
def show_recs():
	displayItems = ShowRecs.testShow()
	# just for debugging
	return render_template('index.html', newBooks=displayItems, oldBooks=displayItems)

@app.route('/')
def add_recs():
	booksToList = AddRecs.testAdd()
	addedBooks = booksToList[0]
	existingBooks = booksToList[1]
	return render_template('index.html', newBooks=addedBooks, oldBooks=existingBooks)