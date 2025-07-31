from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Library, Book
from .forms import RegistrationForm

def list_books(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """Displays details for a specific library,
    listing all books available in the library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        """Will use <pk> from the URL to prefetch all related <books>."""
        return Library.objects.prefetch_related('books')


def register(request):
    """Registers a new user."""
    if request.user.is_authenticated:
        return redirect('list-books')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = RegistrationForm()
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)

def login_user(request):
    """Authenticates a user."""
    if request.user.is_authenticated:
        return redirect('list-books')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list-books')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'relationship_app/login.html', context)

def logout_user(request):
    """Logs a user out."""
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'relationship_app/logout.html')
