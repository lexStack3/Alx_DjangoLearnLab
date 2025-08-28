from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views


router = DefaultRouter()
router.register(r'authors', views.AuthorAPIView, basename='author')
router.register(r'books', views.BookAPIView, basename='book')

urlpatterns = [
    path('token/', obtain_auth_token, name='obtain_auth_token'),
    path('books/list/', views.ListView.as_view(), name='books-list'),
    path('books/detail/<int:pk>/', views.DetailView.as_view(), name='book-detial'),
    path('books/create/', views.CreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', views.UpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', views.DeleteView.as_view(), name='book-delete'),
    path('', include(router.urls))
]
