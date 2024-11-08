from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Note


class NotesTestСase(TestCase):
    """Класс тестирования представлений notes_app"""

    def setUp(self):
        """Настройки теста. Создание тестового пользователя и заметок"""
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.note1 = Note.objects.create(user=self.user,
                                         title='test title1',
                                         text='test text1',
                                         id=1)
        self.note2 = Note.objects.create(user=self.user,
                                         title='test title2',
                                         text='test text2',
                                         id=2)
        self.client = Client()
        self.client.force_login(self.user)

    def test_index(self):
        """Тестирование домашней страницы"""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_notes(self):
        """Тестирование страницы со списком заметок"""
        response = self.client.get('/notes/')
        self.assertEqual(response.status_code, 200)

    def test_note(self):
        """Тестирование страницы отдельной заметки"""
        response = self.client.get('/note/1/')
        self.assertEqual(response.status_code, 200)

    def test_new_note(self):
        """Тестирование страницы создания заметки"""
        response = self.client.get('/new_note/')
        self.assertEqual(response.status_code, 200)

    def test_edit_note(self):
        """Тестирование страницы редактирования заметки"""
        response = self.client.get('/edit_note/1/')
        self.assertEqual(response.status_code, 200)


class NotesAPITestCase(APITestCase):
    """Класс тестирования API notes_app"""

    def setUp(self):
        """Настройки теста. Создание тестового пользователя и заметок"""
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.note1 = Note.objects.create(user=self.user,
                                         title='test title 1',
                                         text='test text 1',
                                         id=1)
        self.note2 = Note.objects.create(user=self.user,
                                         title='test title 2',
                                         text='test text 2',
                                         id=2)
        self.client = Client()
        self.client.force_login(self.user)

    def test_get_notes(self):
        """Тестирование получения всех заметок"""
        response = self.client.get('/api/v1/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['notes']), 2)

    def test_create_note(self):
        """Тестирование создания новой заметки"""
        data = {'title': 'New Note', 'text': 'New text'}
        response = self.client.post('/api/v1/notes/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['note']['title'], data['title'])
        self.assertEqual(response.data['note']['text'], data['text'])

    def test_create_note_missing_fields(self):
        """Тестирование создания заметки с некорректными данными"""
        data = {'title': 'New Note'}
        response = self.client.post('/api/v1/notes/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_access(self):
        """Тестирование доступа без авторизации."""
        logout(self.client)
        response = self.client.get('/api/v1/notes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
