#update book from bookshelf

from bookshelf.models import Book

book = Book.object.get(title=1984)
book.title ="Nineteen Eighty-Four"
book.save()