from app import app
from app.commonFunc import CommonFunctions
from app.addRecords import AddRecords
from app.addManual import AddManual
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

# choose the authors to be added to the db
@app.route('/manual_authors', methods=['POST', 'GET'])
def list_manual_authors():
	gBookIsbnList = request.args['gbooks'] # the request data
	# turn the request data into everything for the page:
	gAuthResults = AddManual.listAuthors(gBookIsbnList)

	return render_template(	'authors_manual_list.html',
							gBookAuths=gAuthResults[0],
							allAuths=gAuthResults[1],
							debugLog=gAuthResults[2])

@app.route('/manual_authors_add', methods=['POST', 'GET'])
def add_manual_authors():
	aNms = request.args.getlist('authNm')
	# do the add
	AddManual.addAuthors(aNms)
	#display the original page
	return str(aNms)

# associate the authors with the books to be added
@app.route('/manual_books', methods=['POST', 'GET'])
def list_manual_books():
	gBookIsbnList = request.args['gbooks'] # the request data
	gBookResults = AddManual.listBooks(gBookIsbnList)
	return render_template('books_manual_list.html',
							gBooks=gBookResults[0],
							allAuths=gBookResults[1],
							debugLog=gBookResults[2])
	return str(gBookResults)