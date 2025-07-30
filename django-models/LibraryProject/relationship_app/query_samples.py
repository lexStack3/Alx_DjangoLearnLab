#!/usr/bin/env python3
"""Testing queries for the Author, Book, Library, and Librarian models
- Query all books by a specific author.
- List all books in a library.
- Retrieve the librarian for a library.
"""
import os, sys, django

# Adding the outer project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setting correct Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Author Instantiations
lewis_caroll, _ = Author.objects.get_or_create(name="Lewis Caroll")
george_martin, _ = Author.objects.get_or_create(name="George R. R. Martin")
francine_rivers, _ = Author.objects.get_or_create(name="Francine Rivers")
charles_perrault, _ = Author.objects.get_or_create(name="Charles Perrault")

# Book Instantiations
wonderland, _ = Book.objects.get_or_create(title="Alice in Wonderland",
                                 author=lewis_caroll)
looking_glass, _ = Book.objects.get_or_create(title="Through the Looking Glass",
                                    author=lewis_caroll)
ice_and_fire, _ = Book.objects.get_or_create(title="The Songs of Ice and Fire",
                                   author=george_martin)
cinderella, _ = Book.objects.get_or_create(title="Cinderella",
                                 author=charles_perrault)
redeeming_love, _ = Book.objects.get_or_create(title="Redeeming Love",
                                     author=francine_rivers)

# Library Instantiations
state_library, _ = Library.objects.get_or_create(name="CRS Library")
state_library.books.set([wonderland, cinderella])

national_library, _ = Library.objects.get_or_create(name="NG Library")
national_library.books.set([wonderland,
                            looking_glass,
                            ice_and_fire,
                            cinderella,
                            redeeming_love])

# Librarian Instantiation
alex, _ = Librarian.objects.get_or_create(name="Alexander Edim", library=national_library)


# Quering all books by a specific author
books = lewis_caroll.books.all()
print("="*40)
print(f"Books by {lewis_caroll.name}")
print("="*40)
for i, book in enumerate(books, start=1):
    print("{}: {} by {}".format(i, book, book.author))

# Listing all books in a library
library = Library.objects.get(name="NG Library")
lib_books = library.books.all()
print("\n" + "="*40)
print(f"Books in {library}")
print("="*40)
for i, book in enumerate(lib_books, start=1):
    print("{}: {} by {}".format(i, book, book.author))

# Retrieves the librarian for a library
librarian = national_library.librarian
print("\n" + "="*40)
print(f"{national_library} Librarian")
print("="*40)
print("The librarian of {} is {}".format(national_library, librarian))
