from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library, Book


def list_books(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """Displays details for a specific library,
    listing all books available in the library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        """Will use <pk> from the URL to prefetch all related <books>."""
        return Library.objects.prefetch_related('books')
