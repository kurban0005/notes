from django.db import models
from django.contrib.auth.models import User
from pyaspeller import YandexSpeller


class Note(models.Model):
    '''Модель заметки.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Возвращает строковое представление модели.'''
        if len(self.title) > 33:
            return f'{self.title[:33]}...'
        else:
            return f'{self.title}'

    def fixe_note(self):
        speller = YandexSpeller()
        self.title = speller.spelled(self.title)
        self.text = speller.spelled(self.text)
        self.save()
        return self
