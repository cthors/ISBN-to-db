from app import app
from app.commonFunc import CommonFunctions
from app.addRecords import AddRecords
from flask import render_template, request

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/list')
def show_records():
	allBooks = CommonFunctions.allBooksForDisplay()
	return render_template('list.html', books=allBooks)

@app.route('/add')
def add_records():
	results = AddRecords.addBook()
	return render_template('list_added.html', 
							newBooks=results[0],
							oldBooks=results[1],
							noBooks=results[2],
							debugList=results[3])

@app.route('/set_lastname/<lname>/<bookId>')
def set_lastname(lname, bookId):
	return "set last name for sort: " + lname + " for " + bookId

@app.route('/<id>')
def one_book_info(id):
	# get the total book json from the id
	bookInfo = CommonFunctions.oneBookInfo(id)
	return render_template('one_book.html', bookInfo=bookInfo)