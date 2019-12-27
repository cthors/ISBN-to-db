class AddRecordsManual():

	def addBooks(bookIsbns):

		booksToAdd = []

		for isbn in bookIsbns:
#			bookJson = getBookJson(isbn)
#
			bookObj = {'title':'', 'subtitle':'', 'authors':'', 'uid':''}
#			item0 = bookJson['items'][0]
#			bookObj['uid'] = item0['id']
#			volumeInfo = item0['volumeInfo']
#			if 'title' in volumeInfo:
#				bookObj['title'] = volumeInfo['title']
#			if 'subtitle' in volumeInfo:
#				bookObj['subtitle'] = volumeInfo['subtitle']
#			if 'authors' in volumeInfo:
#				bookObj['authors'] = volumeInfo['authors']
#
			booksToAdd.append(bookObj)