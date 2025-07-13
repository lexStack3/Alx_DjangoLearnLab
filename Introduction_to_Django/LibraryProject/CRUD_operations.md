# Performing the CRUD operation using Django ORM API
---
## Objectives:
Perform and document each CRUD operation in the Django shell.

---

#### Create:

- Command: Create a Book instance with the title “1984”, author “George Orwell”, and publication year 1949.
- Expected Documentation: Include the Python command and a comment with the expected output noting the successful creation.

#### Solution:
```python
>>> from bookshelf.models import Book
>>>
>>> # Create a Book instance
>>> book = Book(title="1984", author="George Orwell", publication_year=1984)
>>> book.save()
```

---

#### Retrieve:

- Command: Retrieve and display all attributes of the book you just created.
- Expected Documentation: Include the Python command and a comment with the expected output showing the details of the book.
 
#### Solution:
 ```python
 >>> # Retrieve a Book instance with title "1984"
>>> book_1984 = Book.objects.get(title="1984")
>>> book_1984
<Book: 1984>
 ```

---
#### Update:

- Command: Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.
- Expected Documentation: Include the Python command and a comment with the expected output showing the updated title.

#### Solution:
```python
>>> # Updating the title of "1984" to "Nineteen Eighty-Four"
>>> book_1984 = Book.objects.get(title="1984")
>>> # Before update
>>> book_1984
<Book: 1984>
>>> book_1984.title = "Nineteen Eighty-Four"
>>> book_1984.save()
>>> # After update
>>> book_1984
<Book: Nineteen Eighty-Four
```

---
#### Delete:

- Command: Delete the book you created and confirm the deletion by trying to retrieve all books again.
- Expected Documentation: Include the Python command and a comment with the expected output confirming the deletion.

#### Solution:
```python
>>> # Deleting the book "Nineteen Eighty-Four"
>>> book_1984 = Book.objects.get(title="Nineteen Eighty-Four")
>>> book_1984.delete()
(1, {'bookshelf.Book': 1})
>>> # Trying to retrieve deleted item
>>> book_1984 = Book.objects.get(title="Nineteen Eighty-Four")
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/lexstack/ALX_BACKEND/BACKEND_VENV/lib/python3.12/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lexstack/ALX_BACKEND/BACKEND_VENV/lib/python3.12/site-packages/django/db/models/query.py", line 633, in get
    raise self.model.DoesNotExist(
bookshelf.models.Book.DoesNotExist: Book matching query does not exist.
```