from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsOwner


class BookAPIView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CreateView(generics.CreateAPIView):
    """
    Enforces `authentication_classes` for the authentication backend,
    `permission_classes` to make sure that the user is authenticated before
    the user can create a book.
    """
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class UpdateView(generics.UpdateAPIView):
    """
    Enforces `authentication_classes` for the authentication backend,
    `permission_classes` to make sure that the user is authenticated and
    also the owner of the book to update (or adminUser).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serilaizer.data)


class DeleteView(generics.DestroyAPIView):
    """
    Enforces `authentication_classes` for the authentication backend,
    `permission_classes` to make sure that the user is authenticated and
    also the owner of the book to delete the book (or adminUser).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
