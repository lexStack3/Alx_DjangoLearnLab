# Managing Permissions and Groups in Django
---
## About
This example demonstrates how to implement role-based access control in a Django app (`bookshelf`) using groups and custom permissions. The goal is to restrict access to certain actions (viewing, creating, editing, deleting books) based on user roles.

## Objective
- Define custom permissions in the `Book` model.
- Create user groups (`Editors`, `Viewers`, `Admins`) and assign appropriate permissions.
- Create users and assign them to groups.
- Test permissions in the Django shell.

### Step 1: Defining Custom Permissions in the `Book` model
Inside `bookshelf/models.py`
```python
from django.db import models

class Book(models.Model):
    """Model presentation of a book."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        default_permissions = ()
        permissions = (
            ('can_view', 'Can view a book.'),
            ('can_create', 'Can create a book.'),
            ('can_edit', 'Can edit a book.'),
            ('can_delete', 'Can delete a book.')
        )
    
    def __str__(self):
        return self.title
```
Run:
```bash
(env) $ python manage.py makemigrations
(env) $ python manage.py migrate
```

### Step 2: Creating Groups and Assigning Permissions
Open the Django shell
```bash
(env) $ python manage.py shell
```
Then run:

```python
>>> from django.contrib.auth.models import Group, Permission
>>> from django.contrib.contenttypes.models import ContentType
>>> from bookshelf.models import Book
>>>
>>> # Get content type for the Book model
>>> context_type = ContentType.objects.get_for_model(Book)
>>>
>>> # Fetch custom permissions
>>> can_view = Permission.objects.get(codename='can_view', content_type=content_type)
>>> can_create = Permission.objects.get(codename='can_create', content_type=content_type)
>>> can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
>>> can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)
>>>
>>> # Create groups
>>> Editors = Group.objects.create(name='Editors')
>>> Viewers = Group.objects.create(name='Viewers')
>>> Admins = Group.objects.create(name='Admins')
>>>
>>> # Assign permissions
>>> Editors.permissions.set([can_view, can_edit])
>>> Viewers.permissions.add(can_view)
>>> Admins.permissions.set([can_view, can_create, can_edit, can_delete])
```

### Step 3: Creating Users and Assigning to Groups

```python
>>> from django.contrib.auth import get_user_model
>>> # Create new users
>>> User = get_user_model()
>>> manager = User.objects.create_user(username='krab',
...     email='krab@crabypaddy.ocean',
...     password='monimonimonimoni')
>>> cook = User(username='spongebob',
...     email='spongi@gary.com',
...     password='ilovegary')
>>> cashier = User.objects.create_user(username='squidward',
...     email='squidy@bikiny.bottom',
...     password='musical')
>>> customer1 = User.objects.create_user(username='patrick',
...     email='starboy@ocean.ice',
...     password='spongebob')
>>> customer2 = User.objects.create_user(username='plankton',
...     email='fakefriend@tricky.come',
...     password='getrecipe')
>>>
>>> # Assign users to groups
>>> manager.groups.add(Admins)
>>> cook.groups.add(Editors)
>>> cashier.groups.add(Editors)
>>> customer1.groups.add(Viewers)
>>> customer2.groups.add(Viewers)
```

### Step 4: Testing Permissions
```python
>>> # Testing the Admin permissions (must have ALL)
>>> manager.has_perms([
...     'bookshelf.can_view',
...     'bookshelf.can_create',
...     'bookshelf.can_edit',
...     'bookshelf.can_delete'
... ])
True
>>>
>>> # Testing the Editors permissions
>>> cook.has_perms(['bookshelf.can_view', 'bookshelf.can_edit'])
True
>>> cook.has_perm('bookshelf.can_create')
False
>>> cook.has_perm('bookshelf.can_delete')
False
>>>
>>> # Testing the Viewers permissions
>>> customer1.has_perm('bookshelf.can_view')
True
>>> customer2.has_perm('bookshelf.can_view')
True
>>> customer1.has_perm('bookshelf.can_create')
False
>>> customer2.has_perm('bookshelf.can_delete')
False
```

### Note:
Implementing permissions and group-based access control is essential for maintaining application security, enforcing business rules, and ensuring that users can only perform actions appropriate to their roles. Properly defining, assigning, and testing these constraints helps prevent unauthorized access, protects sensitive data, and promotes a clear separation of responsibilities with the system.
