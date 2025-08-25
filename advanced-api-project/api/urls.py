from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'authors', views.AuthorView, basename='author')
router.register(r'books', views.BookView, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
