from app import db

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	json = db.Column(db.String(7000), unique=False, nullable=True)

	def __repr__(self):
		return format(json)
