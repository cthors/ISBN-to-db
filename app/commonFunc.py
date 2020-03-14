from app.models import Book
from string import Template
import requests, json
import pprint

class CommonFunctions():

	##### DISPLAY FUNCTIONS ##########################################################
	# input: a Book object
	# output: the book info, formatted and packaged for book_table.html (the book list display)
	def formatForBookTable(book):
		fullTitle = book._title
		if (book._subtitle):
			fullTitle = book._title + " - " + book._subtitle
		authorNm = ', '.join(map(str, book._authors))
		return {'fullTitle':fullTitle, 'authorNm':authorNm, 'bookId':book._bookId}

	# output: an array of objects
	def allBooksForDisplay():
		displayObj = []
		booksList = Book.query.all()
		for b in booksList:
			displayObj.append(CommonFunctions.formatForBookTable(b))
		return displayObj

	def oneBookInfo(bookId):
		str = Book.query.filter_by(_bookId=bookId).first()._bookJson
		pp = pprint.PrettyPrinter(width=41, compact=True)
		return pp.pprint(str)