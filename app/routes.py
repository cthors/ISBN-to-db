from app import app
from app.commonFunc import CommonFunctions
from app.addRecords import AddRecords
from app.addManual import AddAuthorsManual
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
							gBooks=results[1],
							oldBooks=results[2],
							noBooks=results[3],
							debugList=results[4],
							gBookIds=results[5])

@app.route('/manual_authors', methods=['POST', 'GET'])
def list_manual_authors():
	gBookIsbnList = request.args['gbooks'] # the request data
	# turn the request data into everything for the page:
	gBookResults = AddAuthorsManual.listAuthors(gBookIsbnList)

	return render_template(	'authors_manual_list.html',
							gBookAuths=gBookResults[0],
							allAuths=gBookResults[1],
							debugLog=gBookResults[2])

@app.route('/manual_authors_add', methods=['POST', 'GET'])
def add_manual_authors():
	aNms = request.args.getlist('authNm')
	# do the add
	#display the original page
	return str(aNms)