from django.shortcuts import render
from django.views.generic import ListView
from .models import Book

def list_books(request):
    books = Book.objects.all()
    context = {
        'books': books
    }

    return render(request, 'relationship_app/list_books.html', context)


class ListBooksView(ListView):
    """Displays details for a specific library,
    listing all books available in the library."""
    model = Book
    template_name = 'relationship_app/
