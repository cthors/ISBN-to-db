from app import db
from app.models import Book, Author, BookAuthor
from app.commonFunc import CommonFunctions
from string import Template
import requests, json

#### OPENLIBRARY #################################################################

urlGetKeyFromIsbn = Template('http://openlibrary.org/api/things?query={"type":"/type/edition", "${isbnType}":"${isbn}"}')
urlGetItemFromKey = Template('http://openlibrary.org/api/get?key=${olKey}')

# input: an isbn-13 or isbn-10
# output: the openlibrary.org book key (url argument)
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

# input: an openlibrary.org key (url argument)
# output: the request result json
def getItemJson(olKey):
	url = urlGetItemFromKey.substitute(olKey=olKey)
	result = json.loads(requests.get(url).text)['result']
	if result:
		return result
	else:
		return 0

# input: a book's json object
# output: an array of openlibrary.org keys for that book's authors
def getAuthorsFromBook(bookJson):
	if ('authors' in bookJson):
		authorKeys = []
		for author in bookJson['authors']:
			authorKeys.append(author['key'])
		return authorKeys
	else:
		return 0

# input: a book's json object
# output: an array of openlibrary.org keys for that book's works
def getWorksFromBook(bookJson):
	if('works' in bookJson):
		worksKeys = []
		for work in bookJson['works']:
			worksKeys.append(work['key'])
		return worksKeys
	else:
		return 0

# input: a work's json object
# output: an array of openlibrary.org keys for that work's authors
def getAuthorsFromWork(workJson):
	if('authors' in workJson):
		authorsKeys = []
		for author in workJson['authors']:
			authorsKeys.append(author['author']['key'])
		return authorsKeys
	else:
		return 0

# input: openlibrary key for a book
# output: UID based on the key
def getUIDfromBookKey(bookKey):
	return bookKey[7:]

# input: the openlibrary key of a book which is NOT yet in the local db
# function: creates the Book and associated Author (if necessary), BookAuthor records in local db
# output: 0
def putBookInDb(bookKey):
	debugList = []
	authorsList = []

	# get the book json & create the Book record
	### Book ###
	bookJson = getItemJson(bookKey)
	bookUID = getUIDfromBookKey(bookKey)
	b = Book(_bookId=bookUID, _bookJson=json.dumps(bookJson))
	# list of authors from book record
	authors = getAuthorsFromBook(bookJson)
	if (authors!=0):
		for item in authors:
			authorsList.append(item)
	else:
		debugList.append("No Authors from Book " + bookUID)

	# get the works record - may give more authors - only taking the first work
	works = getWorksFromBook(bookJson)
	if (works!=0):
#		workUID = works[0][7:]
		workJson = getItemJson(works[0])
		b.set_work(json.dumps(workJson))
		# list of authors from work record
		authors = getAuthorsFromWork(workJson)
		if(authors!=0):
			for item in authors:
				authorsList.append(item)
		else:
			debugList.append("No Author from Work for Book " + bookUID)
	else:
		debugList.append("No Works from Book " + bookUID)

	# go through the authors list, remove duplicates, and add the Author and BookAuthor records
	authorsNoDup = list(dict.fromkeys(authorsList))
	for item in authorsNoDup:
		authorUID = item[9:] # the portion of the openlibrary key to use for the db key
		authorJson = getItemJson(item)
		# create the author record if it doesn't already exist
		### Author ###
		authorRecord = Author.query.filter_by(_authorId=authorUID).first()
		if not authorRecord:
			a = Author(_authorId=authorUID, _json=json.dumps(authorJson))
			if 'name' in authorJson:
				a._name = authorJson['name']
			db.session.add(a)
			debugList.append("Added a record for Author " + authorUID)
		### BookAuthor ###
		ba = BookAuthor(_authorId=authorUID, _bookId=bookUID)
		db.session.add(ba)
		debugList.append("Added a BookAuthor record " + authorUID + "," + bookUID)

	# finish up the Book record and add it
	### Book ###
	if 'title' in bookJson:
		b.set_title(bookJson['title'])
	if 'subtitle' in bookJson:
		b.set_subtitle(bookJson['subtitle'])
	db.session.add(b)
	debugList.append("Adding a Book record")
	db.session.commit()
	return 0

##### MAIN ########################################################################

# TODO: should I remove the isbns from the file after adding?

class AddRecords():

	def addBook():
		debugList = []
		booksAddedList = []
		booksExistingList = []
		booksNotFoundList = []
		booksForManualInput = []
		gBookIsbns = []

		f_ISBNlist = open("isbn_list.txt")
		for line in f_ISBNlist:
			if line != '\n':
				# TODO: check if the line is in the proper format
				isbn = line[7:].rstrip() 		# isbn
				bookKey = getBookKey(isbn)		# open library key / url portion
				if(bookKey!=0):
					bookUID = getUIDfromBookKey(bookKey)	# open library key with url portion removed
					bookRecord = Book.query.filter_by(_bookId=bookUID).first()
					if not bookRecord: # book is not in db
						putBookInDb(bookKey)
						bookRecord = Book.query.filter_by(_bookId=bookUID).first()
						booksAddedList.append(CommonFunctions.formatForBookTable(bookRecord))
					else:
						booksExistingList.append(CommonFunctions.formatForBookTable(bookRecord))
				else: # not in openlibrary.org - check google books api
					bookJsonG = CommonFunctions.getBookJsonGoog(isbn)
					if 'totalItems' in bookJsonG:
						if(bookJsonG['totalItems']!=0):
							bookUID = bookJsonG['items'][0]['id']
							# check if it's in the db
							bookRecord = Book.query.filter_by(_bookId=bookUID).first()
							if not bookRecord: # book is not in db
								gBookIsbns.append(isbn)
								# create a temporary object representing the book (for display on this page)
								bookObj = {'fullTitle':'', 'authorNm':''}
								volumeInfo = bookJsonG['items'][0]['volumeInfo']
								if 'title' in volumeInfo:
									bookObj['fullTitle'] = volumeInfo['title']
								if 'subtitle' in volumeInfo:
									bookObj['fullTitle'] = bookObj['fullTitle'] + " " + volumeInfo['subtitle']
								if 'authors' in volumeInfo:
									bookObj['authorNm'] = ', '.join(map(str, volumeInfo['authors']))
								booksForManualInput.append(bookObj)
							else:
								booksExistingList.append(CommonFunctions.formatForBookTable(bookRecord))
						else:
							booksNotFoundList.append("ISBN: " + isbn)
					else: # something weird is wrong (reached API request limit, etc)
						debugList.append(bookJsonG)

		f_ISBNlist.close()
		debugList.append("debugging on")
		gBookIsbnsJson = json.dumps(gBookIsbns)

		return [booksAddedList,
				booksForManualInput,
				booksExistingList,
				booksNotFoundList,
				debugList,
				gBookIsbnsJson]