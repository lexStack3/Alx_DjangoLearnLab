from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime


User = get_user_model()

def current_year():
    return datetime.date.today().year


class Author(models.Model):
    """Model representation of an author instance."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the string representation of an author instnace."""
        return self.name


class Book(models.Model):
    """Model representation of a book instance."""
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(current_year)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_add_book', 'Can Add Book'),
            ('can_change_book', 'Can Change Book'),
            ('can_delete_book', 'Can Delete Book')
        ]

    def __str__(self):
        """Returns the string representation of a book instance."""
        return self.title


class Library(models.Model):
    """Model representation of a library instance."""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the string representation of a library instance."""
        return self.name


class Librarian(models.Model):
    """Model represetation of a librarian instance."""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of a librarian instance."""
        return self.name


class UserProfile(models.Model):
    """Model represetantion of a user_profile instance."""
    ROLE_CHOICES = [
        ('A', 'Admin'),
        ('L', 'Librarian'),
        ('M', 'Member')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        """Returns the string representation of a user_profile instance."""
        return  self.user.username
