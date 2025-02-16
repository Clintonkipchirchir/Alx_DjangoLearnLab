#create Book instance

from bookshelf.models import Book

book = Book.create(title="1984, author="George Orwell", publication_year=1949)