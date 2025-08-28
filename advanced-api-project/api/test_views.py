from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Book, Author
from .serializers import BookSerializer


class TestAPICRUD(APITestCase):

    data = [
        {
            'username': 'lexstack', 
            'password': 'lexpassword',
            'books': [
                {
                    'title': 'The Last Sunrise', 'publication_year': 2010,
                    'author': 'Grace Nwosu'
                },
                {
                    'title': 'Fragments of Tomorrow', 'publication_year': 2017,
                    'author': 'Michael Abiola'
                },
                {
                    'title': 'Beneath the Baobab Tree', 'publication_year': 2003,
                    'author': 'Chinedu Okeke'
                },
                {
                    'title': 'The Crimson Tide', 'publication_year': 2021,
                    'author': 'Fatima Yusuf'
                }
            ]
        },
        {
            'username': 'marvi',
            'password': 'mavpassword',
            'books': [
                {
                    'title': 'The Forgotten Path', 'publication_year': 2018,
                    'author': 'Richard Bassey'
                },
                {
                    'title': 'Storm Over Lagos', 'publication_year': 2020,
                    'author': 'Aisha Bello'
                },
                {
                    'title': 'Echoes in the Valley', 'publication_year': 1995,
                    'author': 'Daniel Eze'
                },
            ]
        },
        {
            'username': 'admin',
            'password': 'strongpassword',
            'books': [
                {
                    'title': 'The Silent Horizon', 'publication_year': 1998,
                    'author': 'Maria Okafor'
                },
                {
                    'title': 'Whispers of the Desert', 'publication_year': 2005,
                    'author': 'James Adeyemi'
                },
                {
                    'title': 'Dancing with Shadows', 'publication_year': 2012,
                    'author': 'Evelyn Chukwu'
                }
            ]
        }
    ]


    @classmethod
    def setUpClass(cls):
        """
        Populating the database.
        """
        super().setUpClass()
        for datum in cls.data:
            books = datum.pop('books')
            user = User.objects.create(**datum)
            for book in books:
                author, _ = Author.objects.get_or_create(name=book.pop('author'))
                Book.objects.create(author=author, owner=user, **book)

    def setUp(self):
        """Setting up neccessary objects for each test case."""
        self.queryset = Book.objects.all()
        self.books = BookSerializer(self.queryset, many=True).data


    def test_book_list(self):
        """Testing the get operation on all books."""
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEqual(self.books, response.data)
        self.assertEqual(len(response.data), self.queryset.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_book_detail(self):
        """Testing the get operation on a specific book."""
        book_1 = self.books[0]
        url = reverse('book-detail', kwargs={'pk': book_1.get('id')})
        response = self.client.get(url)

        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data, book_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_create(self):
        """Testing the create operation of a new book."""
        user = User.objects.get(username='lexstack')
        self.client.force_authenticate(user=user)
        author, _ = Author.objects.get_or_create(name='George R. R. Martin')
        new_book = {'title': 'A Songs of Ice and Fire',
                    'publication_year': 1996,
                    'author': {
                        'id': author.id,
                        'name': author.name}
                    }
        url = reverse('book-create')
        response = self.client.post(url, new_book, format='json')
        new_book['id'] = Book.objects.all().last().id

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, new_book)
        self.assertIsInstance(response.data, dict)

        Book.objects.all().last().delete()

    def test_book_update(self):
        """Testing the patch and update operation on an existing book."""

        # Payload and book to update
        payload = {'title': 'Tom & Jerry'}
        last_book = Book.objects.all().last()
        
        # Loging the owner of the last book.
        user = User.objects.get(pk=last_book.owner.id)
        self.client.force_authenticate(user=user)

        # Testing PATCH operation
        url = reverse('book-update', kwargs={'pk':last_book.id})
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing UPDATE operation
        full_payload = {'title': 'Sun Flowers', 'publication_year': 1923,
                         'author': {
                             'name': 'Peter Pan'
                             }
                         }
        response = self.client.put(url, full_payload, format='json')
        last_book = Book.objects.all().last()
        full_payload['id'] = last_book.id
        full_payload['author']['id'] = response.data['author']['id']

        self.assertEqual(response.data, full_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_delete(self):
        """Testing the delete operation on an existing book."""
        last_book = Book.objects.all().last()
        url = reverse('book-delete', kwargs={'pk': last_book.id})
        user = User.objects.get(pk=last_book.owner.id)
        self.client.force_authenticate(user=user)

        old_count = Book.objects.all().count()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(Book.objects.all().count(), old_count)


class TestCRUDWithoutAuth(APITestCase):
    """Testing `IsAuthenticated` permission on Creating, Updating and Deleting a book."""

    error_msg = {'detail': 'Authentication credentials were not provided.'}
    book = Book.objects.all().last()
    
    def test_book_create_without_auth(self):
        """
        Testing the `IsAuthenticated` permission for createing a
        new book.
        """
        url = reverse('book-create')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, self.error_msg)
    
    def test_book_update_without_auth(self):
        """
        Testing the `IsAuthenticated` permission on updating an existing book.
        """
        url = reverse('book-update', kwargs={'pk': self.book.id})
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, self.error_msg)
    
    def test_book_delete_without_auth(self):
        """
        Testing the `IsAuthenticated` permission on deleting an existing book.
        """
        url = reverse('book-delete', kwargs={'pk': self.book.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.error_msg)


class TestCRUDWithWrongAuth(APITestCase):
    """
    Testing permissions.
    """

    @classmethod
    def setUpClass(cls):
        """Creating a new book for this test.""" 
        super().setUpClass()
        payload = {'title': 'A Songs of Ice and Fire',
                    'publication_year': 1996,
                    'author': {
                        'name': 'Adam Jones'}
                    }
        user = User.objects.create(username="lexstack", password="password")
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('book-create')
        client.post(url, payload, format='json')
        client.logout()

        cls.error_msg = {'detail': 'Please login as the Owner of this book to be able to perform this action.'}
    
    def setUp(self):
        """
        Creates a random_user for testing permissions.
        """
        self.random_user = User.objects.create(username='annoy', password="$Tr0NgP@$$W0Rd")
        self.book = Book.objects.first()

    def test_book_update_with_wrong_auth(self):
        """
        Testing `IsOwner` permission on updating a book instance not
        created by the authenticated user.
        """
        self.client.login(user=self.random_user, password="$Tr0NgP@$$W0Rd")
        url = reverse('book-update', kwargs={'pk': self.book.id})
        payload = {'title': 'Lion King'}
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.book.title, payload.get('title'))

    def test_book_delte_with_wrong_auth(self):
        """
        Testing `IsOwner` permission on deleting a book instance not
        created by the authenticated user.
        """
        self.client.force_authenticate(user=self.random_user)
        url = reverse('book-delete', kwargs={'pk': self.book.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book.id).exists())