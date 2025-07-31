from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

def current_year():
    return datetime.date.today().year


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True
        verbose_name = 'Base Model'


class Author(Base):
    """Model representation of an author instance."""
    name = models.CharField(max_length=100)

    def __str__(self):
        """Returns the string representation of an author instnace."""
        return self.name


class Book(Base):
    """Model representation of a book instance."""
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(current_year)
        ]
    )

    def __str__(self):
        """Returns the string representation of a book instance."""
        return self.title


class Library(Base):
    """Model representation of a library instance."""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        """Returns the string representation of a library instance."""
        return self.name


class Librarian(Base):
    """Model represetation of a librarian instance."""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def __str__(self):
        """Returns a string representation of a librarian instance."""
        return self.name
