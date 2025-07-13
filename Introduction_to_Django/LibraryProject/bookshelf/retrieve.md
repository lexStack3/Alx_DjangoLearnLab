# Retrieve:

- Command: Retrieve and display all attributes of the book you just created.
- Document in: retrieve.md
- Expected Documentation: Include the Python command and a comment with the expected output showing the details of the book.
 ---
 ## Solution:
 ```python
 >>> # Retrieve a Book instance with title "1984"
>>> book_1984 = Book.objects.get(title="1984")
>>> book_1984
<Book: 1984>
 ```