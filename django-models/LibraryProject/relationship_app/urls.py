from django.urls import path
from .views import list_books, LibraryDetailView, UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name='list-books'),
    path('library/<int:pk>', LibraryDetailView.as_view(),
         name='library-detail'),
    path('register/', UserRegistrationForm.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html')
         ,name="login"),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'),
         name="logout")
]
