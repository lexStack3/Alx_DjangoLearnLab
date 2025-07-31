from django.urls import path
from .views import list_books, LibraryDetailView, login_user, logout_user, register

urlpatterns = [
    path('books/', list_books, name='list-books'),
    path('library/<int:pk>', LibraryDetailView.as_view(),
         name='library-detail'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]
