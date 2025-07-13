# Delete:

- Command: Delete the book you created and confirm the deletion by trying to retrieve all books again.
- Document in: delete.md
- Expected Documentation: Include the Python command and a comment with the expected output confirming the deletion.
---
## Solution:
```python
>>> # Deleting the book "Nineteen Eighty-Four"
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> # Trying to retrieve deleted item
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/lexstack/ALX_BACKEND/BACKEND_VENV/lib/python3.12/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lexstack/ALX_BACKEND/BACKEND_VENV/lib/python3.12/site-packages/django/db/models/query.py", line 633, in get
    raise self.model.DoesNotExist(
bookshelf.models.Book.DoesNotExist: Book matching query does not exist.
```