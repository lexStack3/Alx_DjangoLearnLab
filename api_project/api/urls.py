from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
