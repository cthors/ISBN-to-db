from app import app
from app.models import Book, Author, BookAuthor
from flask import render_template
from string import Template
import requests
import json

urlGetKeyFromIsbn = Template('http://openlibrary.org/api/things?query={"type":"/type/edition", "${isbnType}":"${isbn}"}')
urlGetItemFromKey = Template('http://openlibrary.org/api/get?key=${olKey}')

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

def getItem(olKey):
	url = urlGetItemFromKey.substitute(olKey=olKey)
	result = json.loads(requests.get(url).text)['result']
	if result:
		return result
	else:
		return 0

def getAuthorsFromBook(bookJson):
	if ('authors' in bookJson):
		authorKeys = []
		for author in bookJson['authors']:
			authorKeys.append(author['key'])
		return authorKeys
	else:
		return 0

def getWorksFromBook(bookJson):
	if('works' in bookJson):
		worksKeys = []
		for work in bookJson['works']:
			worksKeys.append(work['key'])
		return worksKeys
	else:
		return 0

def getAuthorsFromWork(workJson):
	if('authors' in workJson):
		authorsKeys = []
		for author in workJson['authors']:
			authorsKeys.append(author['author']['key'])
		return authorsKeys
	else:
		return 0

@app.route('/list')
def testdb():
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

	return render_template('index.html', books=displayLines)

@app.route('/')
def hello():

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

			### Book ###
			bookUID = bookKey[7:]
			bookJson = getItem(bookKey)
			# display to page
			books.append(bookJson)
			books.append("Book ID: " + bookUID)
			# create book record if doesn't apready exist
			# todo: leave this whole thing if the book exists already
			dbBook = Book.query.filter_by(bookId=bookUID).first()
			if not dbBook:
				books.append("adding book to db")
#				b = Book(bookUID)
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
						a = Author(id=authorUID, json=authorJson)
#						db.session.add(a)
					##############

					### BookAuthor ###
					# todo: create the record linking the author to the book
					##################
#	db.session.commit()
	f_ISBNlist.close()
	return render_template('index.html', books=books)
