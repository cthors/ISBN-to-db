from app import db
from app.models import Book, Author, BookAuthor
from string import Template
import requests
import json

urlGetKeyFromIsbn = Template('http://openlibrary.org/api/things?query={"type":"/type/edition", "${isbnType}":"${isbn}"}')
urlGetItemFromKey = Template('http://openlibrary.org/api/get?key=${olKey}')

# takes an isbn-13 or isbn-10, returns the openlibrary.org book key (url argument) 
def getBookKey(isbn):
	# try isbn13
	url = urlGetKeyFromIsbn.substitute(isbnType="isbn_13", isbn=isbn)
	result = json.loads(requests.get(url).text)['result']
	if result:
		return result[0]
	else:
		# try isbn10
		url = urlGetKeyFromIsbn.substitute(isbnType="isbn_10", isbn=isbn)
		result = json.loads(requests.get(url).text)['result']
		if result:
			return result[0]
		else:
			return 0

# takes an openlibrary.org key, does a request on that key and returns the json result 
def getItem(olKey):
	url = urlGetItemFromKey.substitute(olKey=olKey)
	result = json.loads(requests.get(url).text)['result']
	if result:
		return result
	else:
		return 0

# takes the json object of a book, returns an array of openlibrary.org keys for the authors of that book
def getAuthorsFromBook(bookJson):
	if ('authors' in bookJson):
		authorKeys = []
		for author in bookJson['authors']:
			authorKeys.append(author['key'])
		return authorKeys
	else:
		return 0

# takes the json object of a book, returns an array of openlibrary.org keys for the works of that book
def getWorksFromBook(bookJson):
	if('works' in bookJson):
		worksKeys = []
		for work in bookJson['works']:
			worksKeys.append(work['key'])
		return worksKeys
	else:
		return 0

# takes the json object of a work, returns an array of openlibrary.org keys for the authors of that work
def getAuthorsFromWork(workJson):
	if('authors' in workJson):
		authorsKeys = []
		for author in workJson['authors']:
			authorsKeys.append(author['author']['key'])
		return authorsKeys
	else:
		return 0

def dispFromDbRecord(bookRecord):
	# TODO: maybe return some author stuff here too
	return bookRecord.bookId

# for books that dont exist in the db, gets the info & puts it in.
# takes bookUID for primary key in db, bookKey for making the request to openlibrary (tho bookUID is easily derived from bookKey)
def putBookInDb(bookKey, bookUID):
	debugList = [""]
	authorsList = []

	### Book ###
	bookJson = getItem(bookKey)
	b = Book(bookId=bookUID, bookJson=json.dumps(bookJson))

	# list of authors from book record
	authors = getAuthorsFromBook(bookJson)
	if (authors!=0):
		for item in authors:
			### Author ###
			authorsList.append(item)
	else:
		debugList.append("No Authors from Book json")

	# works record (only taking the first one)
	works = getWorksFromBook(bookJson)
	if (works!=0):

		### Work ###
		workUID = works[0][7:]
		workJson = getItem(works[0])
		# TODO: add to book record (write function in model)

		# list of authors from work record
		authors = getAuthorsFromWork(workJson)
		if(authors!=0):
			for item in authors:
				### Author ###
				authorsList.append(item)
		else:
			debugList.append("No Author from Work json")
	else:
		debugList.append("No Works from Book json")

	# go through the authors list and remove duplicates
	authorsNoDup = list(dict.fromkeys(authorsList))
	for item in authorsNoDup:
		### Author ###
		authorUID = item[9:] # the portion of the openlibrary key to use for the db key
		authorJson = getItem(item)
		# create the author record if it doesn't already exist
		authorRecord = Author.query.filter_by(authorId=authorUID).first()
		if not authorRecord:
			a = Author(authorId=authorUID, json=json.dumps(authorJson))
			db.session.add(a)
			debugList.append("Adding an Author record")
		### BookAuthor ###
		ba = BookAuthor(author_id=authorUID, book_id=bookUID)
		db.session.add(ba)
		debugList.append("Adding a BookAuthor record")

	### Book ###
	if 'subtitle' in bookJson:
		subTitle = bookJson['subtitle']
		# TODO: add to Book record
	if 'description' in bookJson:
		description = bookJson['description']
		# TODO: add to Book record
	db.session.add(b)
	debugList.append("Adding a Book record")
	db.session.commit()
	return 0

class AddRecs():

	def testAdd():
		debugList = [""]
		booksAddedList = [""]
		booksExistingList = [""]

		# open the file on the server with the list of isbns
		f_ISBNlist = open("isbn_list.txt")
		for line in f_ISBNlist:
			isbn = line[7:].rstrip() 		# isbn
			bookKey = getBookKey(isbn)		# open library key / url portion
			if(bookKey!=0):
				bookUID = bookKey[7:]		# open library key with url portion removed
				bookRecord = Book.query.filter_by(bookId=bookUID).first()
				if not bookRecord: # book is not in db
					putBookInDb(bookKey, bookUID)
					bookRecord = Book.query.filter_by(bookId=bookUID).first()
					booksAddedList.append(dispFromDbRecord(bookRecord))
				else:
					booksExistingList.append(dispFromDbRecord(bookRecord))
			else:
				debugList.append("Book not found in openlibrary")
		f_ISBNlist.close()
		return [booksAddedList, booksExistingList]