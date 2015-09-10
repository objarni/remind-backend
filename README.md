ReMind web service
==================

This web service implements three operations:

1. `add(text, book)`. Save a (unicode) text string to a book.
2. `list(book)`. List the texts of a book.
3. `remove_top(book)`. Remove top item in a book.

The texts are listed in reverse order of add; list text added is
first item returned. Remove always removes the first item in a
book, i.e. the last added text.

The UI for ReMind is implemented by [remind-frontend](https://github.com/objarni/remind-frontend).

Tech
----

Implemented in [Python](http://www.python.org) and [Flask](http://flask.pocoo.org/), with [redis](http://redis.io/) to store book content.

Built with [Heroku](http://heroku.com/) deployment in mind.

