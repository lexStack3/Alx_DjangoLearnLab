from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework import filters

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsOwner

from django_filters import rest_framework


class BookAPIView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ListView(generics.ListAPIView):
    queryset = Book.objects.prefetch_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, \
        filters.SearchFilter, filters.OrderingFilter \
    ]
    filterset_fields = {
        'title': ['exact', 'icontains', 'istartswith'],
        'publication_year': ['exact', 'gte', 'lte'],
        'author__name': ['exact', 'icontains', 'istartswith']
    }
    search_fields = ['title', 'publication_year', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']


class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.prefetch_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CreateView(generics.ListCreateAPIView):
    """
    Enforces `authentication_classes` for the authentication backend,
    `permission_classes` to make sure that the user is authenticated before
    the user can create a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class UpdateView(generics.RetrieveUpdateAPIView):
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
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DeleteView(generics.RetrieveDestroyAPIView):
    """
    Enforces `authentication_classes` for the authentication backend,
    `permission_classes` to make sure that the user is authenticated and
    also the owner of the book to delete the book (or adminUser).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
