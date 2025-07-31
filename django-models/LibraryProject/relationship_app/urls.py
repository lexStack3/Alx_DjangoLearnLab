from django.urls import path
from .view import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list-books'),
    path('library/<int:pk>', LibraryDetailView.as_view(),
         name='library-detail'),
]
