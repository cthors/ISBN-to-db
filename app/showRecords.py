from app.models import Book, Author, BookAuthor

class ShowRecs():
	def testShow():
		displayLines = []

		displayLines.append("BOOKS:")
		booksList = Book.query.all()
		displayLines.append(booksList)

		displayLines.append("AUTHORS:")
		authorsList = Author.query.all()
		displayLines.append(authorsList)

		displayLines.append("BOOK AUTHORS:")
		bookAuthorsList = BookAuthor.query.all()
		displayLines.append(bookAuthorsList)
		return displayLines