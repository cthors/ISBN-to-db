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

@app.route('/<id>')
def one_book_info(id):
	return render_template('one_book.html', bookId=id)
#	return render_template('one_book.html', bookId="yup")