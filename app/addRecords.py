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

class AddRecs():

	def testAdd():

		books = []
		# open the file on the server with the list of isbns
		f_ISBNlist = open("isbn_list.txt")
		for line in f_ISBNlist:
			books.append("-------------------------------")
			isbn = line[7:].rstrip()
			books.append("ISBN: "+ isbn)
			bookKey = getBookKey(isbn)
			authorsList = []

			if(bookKey!=0):

				# get the book ID
				# if exists in db:
				#	get book info from db
				#	add to right column
				# if doesn't exist in db:
				#	get book info from request
				# 	add to left column
				#	add to db

				### Book ###
				bookUID = bookKey[7:]
				bookJson = getItem(bookKey)
				title = bookJson['title']
				if 'subtitle' in bookJson:
					subTitle = bookJson['subtitle']
					books.append(subTitle)
				if 'description' in bookJson:
					description = bookJson['description']
					books.append(description)
				# display to page
				books.append(bookJson)
				books.append("Book ID: " + bookUID + " " + title)
				# create book record if doesn't apready exist
				# todo: leave this whole thing if the book exists already
				dbBook = Book.query.filter_by(bookId=bookUID).first()
				if not dbBook:
					books.append("adding book to db")
					b = Book(bookId=bookUID, bookJson=json.dumps(bookJson))
					db.session.add(b)
				############

					# list of authors from book record
					authors = getAuthorsFromBook(bookJson)
					if (authors!=0):
						for item in authors:
							### Authors ###
							authorsList.append(item)
							###############
					else:
						books.append("no author from book")

					# works record (only taking the first one)
					works = getWorksFromBook(bookJson)
					if (works!=0):

						### Work ###
						workUID = works[0][7:]
						workJson = getItem(works[0])
						# display to page
						books.append("Work ID: " + workUID)
						books.append(workJson)
						# todo: add to book record
						############

						# list of authors from work record
						authors = getAuthorsFromWork(workJson)
						if(authors!=0):
							for item in authors:

								### Authors ###
								authorsList.append(item)
								###############
						else:
							books.append("no author from work")
					else:
						books.append("no works")

					# go through the authors list and remove duplicates
					authorsNoDup = list(dict.fromkeys(authorsList))
					for item in authorsNoDup:

						### Author ###
						authorUID = item[9:]
						authorJson = getItem(item)
						# display to page
						books.append("Author ID: " + authorUID)
						books.append(authorJson)
						# create the author record if it doesn't already exist
						dbAuthor = Author.query.filter_by(authorId=authorUID).first()
						if not dbAuthor:
							books.append("adding an author")
							a = Author(authorId=authorUID, json=json.dumps(authorJson))
							db.session.add(a)
						##############

						### BookAuthor ###
						ba = BookAuthor(author_id=authorUID, book_id=bookUID)
						db.session.add(ba)
						##################

					# add the Book, Author, BookAuthor records to the db
					db.session.commit()
		f_ISBNlist.close()
		return books