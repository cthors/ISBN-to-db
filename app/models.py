from app import db
from sqlalchemy.orm import relationship

class Book(db.Model):
	_id = db.Column(db.Integer, primary_key=True, unique=True)
	_bookId = db.Column(db.String(20), unique=True, nullable=False)
	_bookJson = db.Column(db.String(7000), unique=False, nullable=True)
	_workJson = db.Column(db.String(7000), unique=False, nullable=True)
	_title = db.Column(db.String(200), unique=False, nullable=True)
	_subtitle = db.Column(db.String(200), unique=False, nullable=True)
	# relationships:
	_bookAuthors = relationship("BookAuthor")

	# getter & setters:
	# TODO: switch to @hybrid_property and .setter syntax
	def set_title(self, title):
		self._title = title
	def set_subtitle(self, subtitle):
		self._subtitle = subtitle
	def set_work(self, json):
		self._workJson = json

	# toString
	def __repr__(self):
		return format(self._bookId)

class Author(db.Model):
	_id = db.Column(db.Integer, primary_key=True, unique=True)
	_authorId = db.Column(db.String(20), unique=True, nullable=False)
	_json = db.Column(db.String(7000), unique=False, nullable=True)
	_name = db.Column(db.String(7000), unique=False, nullable=True)

	def __repr__(self):
		return format(self._authorId)

class BookAuthor(db.Model):
	_id = db.Column(db.Integer, primary_key=True, unique=True)
	_authorId = db.Column(db.String(20), db.ForeignKey('author._authorId'))
	_bookId = db.Column(db.String(20), db.ForeignKey('book._bookId'))
	# relationships:
	_authors = relationship("Author")

	def __repr__(self):
		return format(self._id)
