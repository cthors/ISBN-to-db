CREATE TABLE book (
	_id INTEGER NOT NULL, 
	"_bookId" VARCHAR(20), 
	"_bookJson" VARCHAR(7000), 
	"_workJson" VARCHAR(7000), 
	_title VARCHAR(200), 
	_subtitle VARCHAR(200), 
	PRIMARY KEY (_id), 
	UNIQUE (_id), 
	UNIQUE ("_bookId")
);
CREATE TABLE author (
	_id INTEGER NOT NULL, 
	"_authorId" VARCHAR(20), 
	_json VARCHAR(7000), 
	_name VARCHAR(7000), 
	PRIMARY KEY (_id), 
	UNIQUE (_id), 
	UNIQUE ("_authorId")
);
CREATE TABLE book_author (
	_id INTEGER NOT NULL, 
	"_authorId" VARCHAR(20), 
	"_bookId" VARCHAR(20), 
	PRIMARY KEY (_id), 
	UNIQUE (_id), 
	FOREIGN KEY("_authorId") REFERENCES author ("_id"), 
	FOREIGN KEY("_bookId") REFERENCES book ("_id")
);