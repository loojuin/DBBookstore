CREATE TABLE Customer (
	login_name VARCHAR(16) PRIMARY KEY,
    pwd VARCHAR(8),
    surname VARCHAR(16),
    given_name VARCHAR(64),
    creditcard VARCHAR(16),
    address VARCHAR(128),
    phoneno INTEGER
);

CREATE TABLE Book (
	isbn CHAR(14) PRIMARY KEY,
    title VARCHAR(128),
    author VARCHAR(128),
    frmt CHAR(9) CHECK (frmt = "hardcover" OR frmt = "softcover"),
    publisher VARCHAR(64),
    yr INTEGER CHECK (yr > 0),
    sbj VARCHAR(64),
    keywords VARCHAR(128),
    price REAL,
    copies INTEGER
);

CREATE TABLE Ord (
	customer VARCHAR(16),
    book CHAR(14),
    ts CHAR(19),
    oid INTEGER AUTO_INCREMENT UNIQUE,
    qty INTEGER,
    stat VARCHAR(16),
    PRIMARY KEY (customer, book, ts),
    FOREIGN KEY (customer) REFERENCES Customer(login_name),
    FOREIGN KEY (book) REFERENCES Book(isbn)
);

CREATE TABLE Opinion (
	customer VARCHAR(16),
    book CHAR(14),
    score INTEGER CHECK(score >= 0 AND score <= 10),
    txt VARCHAR(256),
    PRIMARY KEY (customer, book),
    FOREIGN KEY (customer) REFERENCES Customer(login_name),
    FOREIGN KEY (book) REFERENCES Book(isbn)
);

CREATE TABLE Rate (
	rater VARCHAR(16),
    ratee VARCHAR(16),
    book CHAR(14),
    rating INTEGER CHECK (rating >=0 AND rating <= 2),
    PRIMARY KEY (rater, ratee, book),
    FOREIGN KEY (rater) REFERENCES Customer(login_name),
    FOREIGN KEY (ratee) REFERENCES Opinion(customer),
    FOREIGN KEY (book) REFERENCES Opinion(book)
);
