from app import db
from app.models import Author
from app.commonFunc import CommonFunctions
from string import Template
import requests, json, re

class AddAuthorsManual():

	# display the author names from the isbn's
	def listAuthors(bookIsbns):
		authorDispObjs = []
		allDbAuthors = Author.query.all()
		debugLog = []

		bookIsbnsJson = json.loads(bookIsbns)

		for isbn in bookIsbnsJson:
			bookJson = CommonFunctions.getBookJsonGoog(isbn)	
			if 'items' in bookJson:
				volumeInfo = bookJson['items'][0]['volumeInfo']
				if 'authors' in volumeInfo:
					for author in volumeInfo['authors']:
						authorDisp = {'title':'','author':''}
						authorDisp['author'] = author
						if 'title' in volumeInfo:
							authorDisp['title'] = volumeInfo['title']
						authorDispObjs.append(authorDisp)
				else:
					debugLog.append("no authors for ISBN " + isbn)
			else: # reached google books API request limit or something
				debugLog.append(bookJson)

		return [authorDispObjs, allDbAuthors, debugLog]

#	lastName = re.split(r'\s|-', author)[-1]
#	namesLike = '%'+ lastName +'%'
#	similarNames = Author.query.filter(Author._name.like(namesLike)).all()

	def addAuthors(authNms):
		return 0
#		for name in authNms:
#			a = Author(_authorId=authorUID)
#			db.session.add(a)
#			db.session.commit()
