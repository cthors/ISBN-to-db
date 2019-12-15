from app import db

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bookId = db.Column(db.String(20), unique=True, nullable=True)
	bookJson = db.Column(db.String(7000), unique=False, nullable=True)
	workJson = db.Column(db.String(7000), unique=False, nullable=True)

	def __repr__(self):
		return format(self.bookJson)

	def set_work(self, json):
		self.workJson = json

class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	authorId = db.Column(db.String(20), unique=True, nullable=True)
	json = db.Column(db.String(7000), unique=False, nullable=True)

	def __repr__(self):
		return format(self.json)

class BookAuthor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.String(20), db.ForeignKey('author.authorId'))
	book_id = db.Column(db.String(20), db.ForeignKey('book.bookId'))

	def __repr__(self):
		return format(self.author_id + " " + self.book_id)
