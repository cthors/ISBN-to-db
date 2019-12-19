from app import db
from app.models import Book, Author, BookAuthor

class ShowRecs():

	# TODO: merge this with the function in addRecords
	def testShow():

		displayObj = []

		booksListQuery = 	db.session.query(Book, BookAuthor, Author).\
							filter(Book._bookId==BookAuthor._bookId).\
							filter(BookAuthor._authorId==Author._authorId)
		booksList = booksListQuery.all()
		for b, ba, a in booksList:
			fullTitle = b._title
			if (b._subtitle):
				fullTitle = b._title + " - " + b._subtitle
			displayObj.append({'fullTitle':str(fullTitle), 'authorNm':b._bookAuthors})
#			displayObj.append({'fullTitle':str(fullTitle), 'authorNm':str(a._name)})
		return displayObj

#		displayLines.append("BOOKS:")
#		booksList = Book.query.all()
#		displayLines.append(booksList)
#
#		displayLines.append("AUTHORS:")
#		authorsList = Author.query.all()
#		displayLines.append(authorsList)
#
#		displayLines.append("BOOK AUTHORS:")
#		bookAuthorsList = BookAuthor.query.all()
#		displayLines.append(bookAuthorsList)