from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('books/', list_books, name='list-books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(),
         name='library-detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login-user/', LoginView.as_view(template_name="relationship_app/login.html",
                                     redirect_authenticated_user=True),
         name='login-user'),
    path('logout-user/', LogoutView.as_view(template_name="relationship_app/logout.html"),
         name='logout-user'),
    path('register/', views.register, name='register'),
]
