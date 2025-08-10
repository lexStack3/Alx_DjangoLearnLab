from relationship_app.models import Book
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_year')
