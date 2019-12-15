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
			books.append("Book ID: " + bookUID)
			bookJson = getItem(bookKey)
			books.append(bookJson)
			# check to see if book is in db - add if not
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
				books.append("Work ID: " + workUID)
				books.append(workJson)
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

			### Authors ###
			authorUID = item[9:]
			books.append("Author ID: " + authorUID)
			authorJson = getItem(item)
			books.append(authorJson)
			# check to see if author is in db - add if not
			# add BookAuthor record to db
			###############

	f_ISBNlist.close()
	return render_template('index.html', books=books)
