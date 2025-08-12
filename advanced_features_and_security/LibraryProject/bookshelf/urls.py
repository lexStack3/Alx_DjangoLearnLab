from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_books, name='list-books'),
    path('create_book/', views.create_book, name='create-book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit-book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete-book')
]
