Update:

- Command: Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.
- Document in: update.md
- Expected Documentation: Include the Python command and a comment with the expected output showing the updated title.
---
# Solution:
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