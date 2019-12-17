CREATE TABLE book (
	id INTEGER NOT NULL, 
	"bookId" VARCHAR(20), 
	"bookJson" VARCHAR(7000), 
	"workJson" VARCHAR(7000), "title" VARCHAR(200), 
	PRIMARY KEY (id), 
	UNIQUE ("bookId")
);
CREATE TABLE author (
	id INTEGER NOT NULL, 
	"authorId" VARCHAR(20), 
	json VARCHAR(7000), 
	PRIMARY KEY (id), 
	UNIQUE ("authorId")
);
CREATE TABLE book_author (
	id INTEGER NOT NULL, 
	author_id VARCHAR(20), 
	book_id VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES author ("authorId"), 
	FOREIGN KEY(book_id) REFERENCES book ("bookId")
);
