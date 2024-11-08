from django.urls import path
from . import views

app_name = 'notes_app'
urlpatterns = [
    # Домашняя страница.
    path('', views.index, name='index'),
    # Страница всех заметок
    path('notes/', views.notes, name='notes'),
    # Страница отдельной заметки
    path('note/<int:note_id>/', views.note, name='note'),
    # Новая заметка
    path('new_note/', views.new_note, name='new_note'),
    # Редактирование заметки
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),

]
