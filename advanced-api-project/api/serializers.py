from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """A Book model serializer."""
    author = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Validating that a user dosen't input
        a year greater than the current year.
        """
        current_year = datetime.today.year
        if value > current_year:
            raise serializers.ValidationError(
                    'Publication year can not be in the future.'
                    )


class AuthorSerializer(serializers.ModelSerializer):
    """An Author model serializer."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
