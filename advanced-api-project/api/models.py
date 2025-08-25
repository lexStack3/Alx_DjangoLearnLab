from django.db import models


class Author(models.Model):
    """A model representation of Author."""
    name = models.CharField(max_length=256)

    def __str__(self):
        """Returns a string representation of a Author instance."""
        return self.name


class Book(models.Model):
    """A model representation of Book."""
    title = models.CharField(max_length=256)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of a Book instance."""
        return f"{self.title} - {self.publication_year} by {self.author.name}"
