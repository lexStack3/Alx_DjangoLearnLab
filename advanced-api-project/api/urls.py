from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'authors', views.AuthorAPIView, basename='author')
router.register(r'books', views.BookAPIView, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('book_list/', views.ListView.as_view(), name='books-list'),
    path('book_detail/<int:pk>/', views.DetailView.as_view(), name='book-detial'),
    path('book_create/', views.CreateView.as_view(), name='book-create'),
    path('book_update/<int:pk>/', views.UpdateView.as_view(), name='book-update'),
    path('book_delete/<int:pk>/', views.DeleteView.as_view(), name='book-delete'),
]
