from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    context = {
        'title': 'Book List',
        'books': books
    }
    return render(request, 'bookshelf/list_books.html', context)

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        book = BookForm(request.POST)
        if book.is_valid():
            book.save()
            return redirect('book-list')
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
            print("\n\nis valid...\n\n")
            form.save()
            return redirect('book-list')
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
    return redirect('book-list')
