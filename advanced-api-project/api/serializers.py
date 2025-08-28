from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """A Book model serializer."""
    class AuthorWriter(serializers.ModelSerializer):
        class Meta:
            model = Author
            fields = ['id', 'name']

    author = AuthorWriter()

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Validating that a user dosen't input
        a year greater than the current year.
        """
        current_year = datetime.today().year
        if value > current_year:
            raise serializers.ValidationError(
                    'Publication year can not be in the future.'
                    )
        return value

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, _ = Author.objects.get_or_create(**author_data)
        return Book.objects.create(author=author, **validated_data)


    def update(self, instance, validated_data):
        """
        Makes sure that the author field is updated appropraitely.
        """
        author_data = validated_data.pop('author', None)
        if author_data:
            instance.author, _ = Author.objects.get_or_create(**author_data)

        instance.title = validated_data.get('title', instance.title)
        instance.publication_year = validated_data.get(
                                        'publication_year',
                                        instance.publication_year
                                    )
        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    """An Author model serializer."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
