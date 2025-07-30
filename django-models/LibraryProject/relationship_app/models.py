from django.db import models


class Author(models.Model):
    """Model representation of an author instance."""
    name = models.CharField(max_length=100)

    def __str__(self):
        """Returns the string representation of an author instnace."""
        return self.name


class Book(models.Model):
    """Model representation of a book instance."""
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        """Returns the string representation of a book instance."""
        return self.title


class Library(models.Model):
    """Model representation of a library instance."""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        """Returns the string representation of a library instance."""
        return self.name


class Librarian(models.Model):
    """Model represetation of a librarian instance."""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def __str__(self):
        """Returns a string representation of a librarian instance."""
        return self.name
