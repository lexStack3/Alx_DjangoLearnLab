from django.db import models


class Book(models.Model):
    """A models representation of a Book."""
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)

    def __str__(self):
        """Returns the string representation of a Book instance."""
        return f"{self.title} by {self.author}"
