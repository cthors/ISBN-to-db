CREATE TABLE book (
	id INTEGER NOT NULL, 
	bookId VARCHAR(20) NOT NULL, 
	bookJson VARCHAR(7000), 
	workJson VARCHAR(7000),
	title VARCHAR(200), 
	subtitle VARCHAR(200), 
	PRIMARY KEY (id), 
	UNIQUE ("bookId")
);
CREATE TABLE author (
	id INTEGER NOT NULL, 
	authorId VARCHAR(20) NOT NULL, 
	json VARCHAR(7000), 
	name VARCHAR(200),
	PRIMARY KEY (id), 
	UNIQUE ("authorId")
);
CREATE TABLE book_author (
	id INTEGER NOT NULL, 
	authorId VARCHAR(20) NOT NULL, 
	bookId VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(authorId) REFERENCES author (authorId), 
	FOREIGN KEY(bookId) REFERENCES book (bookId)
);
