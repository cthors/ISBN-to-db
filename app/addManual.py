from string import Template
import requests, json, re
from app.models import Author

# TODO: combine this with its exact copy in addRecords.py
def getBookGoogleJson(isbn):
	urlGetBookJsonGoogle = Template('https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}')#&key=${API_KEY}')
	url = urlGetBookJsonGoogle.substitute(isbn=isbn, API_KEY='AIzaSyBOKLCMsicjEmjL_lhIWo3TC9Oo_3GJ22s')
	result = json.loads(requests.get(url).text)
	if result:
		return result
	else:
		return 0

class AddRecordsManual():

	def addBooks(bookIsbns):
		booksToAdd = []
		debugLog = []
		authorsInDb = Author.query.all()

		bookIsbnsJson = json.loads(bookIsbns)

		for isbn in bookIsbnsJson:
			debugLog.append(isbn) # debugging
			bookJson = getBookGoogleJson(isbn)
			similarNames = []
			bookObj = {'title':'', 'subtitle':'', 'authors':'', 'uid':'', 'authorsInDb':''}

			if 'items' in bookJson:
				item0 = bookJson['items'][0]
				bookObj['uid'] = item0['id']
				volumeInfo = item0['volumeInfo']
				if 'title' in volumeInfo:
					bookObj['title'] = volumeInfo['title']
				if 'subtitle' in volumeInfo:
					bookObj['subtitle'] = volumeInfo['subtitle']
				if 'authors' in volumeInfo:
					bookObj['authors'] = volumeInfo['authors']
					for author in bookObj['authors']:
						lastName = re.split(r'\s|-', author)[-1]
						namesLike = '%'+ lastName +'%'
						similarNames = Author.query.filter(Author._name.like(namesLike)).all()
				bookObj['authorsInDb'] = str(similarNames)
				booksToAdd.append(bookObj)

			else:
				debugLog.append(bookJson)

		return [booksToAdd, authorsInDb, debugLog]