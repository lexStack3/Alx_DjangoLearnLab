from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm, ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    context = {
        'title': 'Book List',
        'books': books
    }
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        book = BookForm(request.POST)
        if book.is_valid():
            book.save()
            return redirect('bookshelf:book-list')
    form = BookForm()
    context = {
        'title': 'Book Creation',
        'form': form
    }
    return render(request, 'bookshelf/create_book.html', context)

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book-list')
    form = BookForm(instance=book)
    context = {
        'title': 'Edit Book',
        'book': book,
        'form': form
    }
    return render(request, 'bookshelf/edit_book.html', context)

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('bookshelf:book-list')

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def form_example(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book-list')
    form = ExampleForm()
    context = {
        'title': 'Form Example',
        'form': form
    }
    return render(request, 'bookshelf/form_example.html', context)
