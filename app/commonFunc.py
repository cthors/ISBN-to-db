from app.models import Book
from string import Template
import requests, json

class CommonFunctions():

	##### DISPLAY FUNCTIONS ##########################################################
	# input: a Book object
	# output: the book info, formatted and packaged for book_table.html (the book list display)
	def formatForBookTable(book):
		fullTitle = book._title
		if (book._subtitle):
			fullTitle = book._title + " - " + book._subtitle
		authorNm = ', '.join(map(str, book._authors))
		return {'fullTitle':fullTitle, 'authorNm':authorNm}

	# output: an array of objects
	def allBooksForDisplay():
		displayObj = []
		booksList = Book.query.all()
		for b in booksList:
			displayObj.append(CommonFunctions.formatForBookTable(b))
		return displayObj

	##### GOOGLE #####################################################################
	# input: an isbn
	# output: the book's json result from google books api
	def getBookJsonGoog(isbn):
		urlGetBookFromGoogle = Template('https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}')#&key=${API_KEY}')
		url = urlGetBookFromGoogle.substitute(isbn=isbn, API_KEY='AIzaSyBOKLCMsicjEmjL_lhIWo3TC9Oo_3GJ22s')
		result = json.loads(requests.get(url).text)
		if result:
			return result
		else:
			return 0