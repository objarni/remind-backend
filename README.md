ReMind web service
==================

This web service implements three operations:

	list(book)		- list content of book
	add(text, book)		- save unicode text to book
	remove_top(book)	- remove top item in book

The texts are listed in reverse order of add; list text added is
first item returned.

Remove always removes the first item in a book, i.e. the last
added text.

Tech
----

Implemented in Python+Flask, with redis as storage service.

Built with Heroku deployment in mind.

