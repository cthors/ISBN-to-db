from app import app
from flask import render_template
from string import Template
import requests
import json

@app.route('/')
def hello():
	# url, ready to stick in the isbn or openlibrary book ID
	openLibUrl10 = Template('http://openlibrary.org/api/things?query={"type":"/type/edition", "isbn_10":"${isbn}"}')
	openLibUrl13 = Template('http://openlibrary.org/api/things?query={"type":"/type/edition", "isbn_13":"${isbn}"}')
	openLibUrl = Template('http://openlibrary.org/api/get?key=${olId}')
	books = []

	# open the file on the server with the list of isbns
	f_ISBNlist = open("isbn_list.txt")
	for line in f_ISBNlist:
		# make the urls from the current isbn
		currReqUrl10 = openLibUrl10.substitute(isbn=line.rstrip())
		currReqUrl13 = openLibUrl13.substitute(isbn=line.rstrip())

		rawRes13 = requests.get(currReqUrl13).text
		jsonRes13 = json.loads(rawRes13)
		if not jsonRes13['result']:
			rawRes10 = requests.get(currReqUrl10).text
			jsonRes10 = json.loads(rawRes10)
			if not jsonRes10['result']:
				books.append("ISBN not found")
			else:
				currReqUrl = openLibUrl.substitute(olId=jsonRes10['result'][0])
				rawRes = requests.get(currReqUrl).text
				books.append(rawRes)
		else:
			currReqUrl = openLibUrl.substitute(olId=jsonRes13['result'][0])
			rawRes = requests.get(currReqUrl).text
			books.append(rawRes)
	f_ISBNlist.close()
	# create objects based on the returned json
	# add the objects to a table in the database
	# display the records from the database
	return render_template('index.html', books=books)
