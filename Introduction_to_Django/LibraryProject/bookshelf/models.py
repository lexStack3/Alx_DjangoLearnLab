from django.db import models


class Book(models.Model):
    """Model representation of a book."""

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """String representation of a Book instance."""
        return self.title
