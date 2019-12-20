from app.models import Book

class ShowRecords():

	# returns the book info, formatted and packaged for book_table.html (the book list display)
	def formatForBookTable(book):
		fullTitle = book._title
		if (book._subtitle):
			fullTitle = book._title + " - " + book._subtitle
		authorNm = ', '.join(map(str, book._authors))
		return {'fullTitle':fullTitle, 'authorNm':authorNm}

	# returns an array of objects
	def allBooksForDisplay():

		displayObj = []
		booksList = Book.query.all()

		for b in booksList:
			displayObj.append(ShowRecords.formatForBookTable(b))

		return displayObj