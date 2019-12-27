from app import app
from app.showRecords import ShowRecords
from app.addRecords import AddRecords
from flask import render_template
from flask import request

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
							debugList=results[3],
							googleBooks=results[4],
							authors=results[5],
							googleBookIds=results[6])

@app.route('/manual_add', methods=['POST', 'GET'])
def add_recs_google():
	# come here from add_recs... books json needs to be sorted out
	stuff = request.args['testdata']
	return render_template('manual_add_google.html', stuff=stuff)