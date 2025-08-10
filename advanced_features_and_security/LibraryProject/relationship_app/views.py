from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import permission_required
from .models import Library, Book
from .forms import BookForm


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = UserCreationForm()
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

def logged_out_view(request):
    return render(request, 'relationship_app/logout.html')


#===============================================================
#           IMPLEMENTING ROLE-BASED ACCESS CONTROL
#===============================================================

def lazy_checker(role):
    return reverse_lazy('checker', kwargs={'wrong_role': role})

@user_passes_test(lambda user: user.userprofile.role == 'Admin',
                  login_url=lazy_checker('Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(lambda user: user.userprofile.role == 'Librarian',
                  login_url=lazy_checker('Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(lambda user: user.userprofile.role == 'Member',
                  login_url=lazy_checker('Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

def checker_view(request, wrong_role):
    context = {'wrong_role': wrong_role}
    return render(request, 'relationship_app/checker_view.html', context)


#=================================================================
#                 IMPLEMENTING CUSTOM PERMISSIONS
#=================================================================
@permission_required('relationship_app.can_add_book')
def book_add(request):
    """Creates a new book."""
    if request.method == 'POST':
        book = BookForm(request.POST)
        if book.is_valid():
            book.save()
            return redirect('list-books')
    form = BookForm()
    context = {'form': form}
    return render(request, 'relationship_app/book_add.html', context)

@permission_required('relationship_app.can_change_book')
def book_change(request, pk):
    """Updates an existing book by primary book."""
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book = BookForm(request.POST, instance=book)
        if book.is_valid():
            book.save()
            return redirect('list-books')
    form = BookForm(instance=book)
    context = {'form': form}
    return render(request, 'relationship_app/book_change.html', context)

@permission_required('relationship_app.can_delete_book')
def book_delete(request, pk):
    """Deletes a book by its primary key."""
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('list-books')
