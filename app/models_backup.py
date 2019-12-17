from app import db

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bookId = db.Column(db.String(20), unique=True, nullable=True)
	bookJson = db.Column(db.String(7000), unique=False, nullable=True)
	workJson = db.Column(db.String(7000), unique=False, nullable=True)
	title = db.Column(db.String(200), unique=False, nullable=True)
#	subtitle = db.Column(db.String(200), unique=False, nullable=True)

	# getter & setter:
	def set_work(self, json):
		self.workJson = json

#	_workJson = db.Column(db.String(7000), unique=False, nullable=True)
#	@hybrid_property
#	def workJson(self):
#		return self._workJson
#
#	@workJson.setter
#	def workJson(self, workJson):
#		self._workJson = workJson

	# toString
	def __repr__(self):
		return format(self.bookId)

class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	authorId = db.Column(db.String(20), unique=True, nullable=True)
	json = db.Column(db.String(7000), unique=False, nullable=True)

	def __repr__(self):
		return format(self.authorId)

class BookAuthor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.String(20), db.ForeignKey('author.authorId'))
	book_id = db.Column(db.String(20), db.ForeignKey('book.bookId'))

	def __repr__(self):
		return format(self.id)
