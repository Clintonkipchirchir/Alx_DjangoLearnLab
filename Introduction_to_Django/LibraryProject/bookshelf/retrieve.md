# get book from bookshelf

from bookshelf.models import Book

book = Book.object.get(title="1984", author=“George Orwell, publication_year=1949)