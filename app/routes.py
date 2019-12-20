from app import app
from app.showRecords import ShowRecords
from app.addRecords import AddRecords
from flask import render_template

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/list')
def show_recs():
	allBooks = ShowRecords.allBooksForDisplay()
	return render_template('list.html', books=allBooks)

@app.route('/add')
def add_recs():
	results = AddRecords.addBook()
	return render_template('list_added.html', 
							newBooks=results[0],
							oldBooks=results[1],
							noBooks=results[2],
							debugList=results[3])