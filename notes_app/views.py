from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NotesSerializer
from .models import Note
from .forms import NoteForm


class NotesAPIView(APIView):
    '''API класс для модели Note'''
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Получить все заметки'''
        notes_all = Note.objects.filter(user=self.request.user)
        return Response({'notes': NotesSerializer(notes_all, many=True).data})

    def post(self, request):
        '''Создание заметки,'''
        title = request.data.get('title')
        text = request.data.get('text')
        if not title or not text:
            return Response({'error': 'Title and text are required'}, status=400)
        new_note = Note.objects.create(user=request.user, title=title, text=text)
        new_note.fixe_note()
        serializer = NotesSerializer(data={'title': new_note.title, 'text': new_note.text})
        if serializer.is_valid():
            return Response({'note': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)


class EditNoteAPIView(APIView):
    def post(self, request, pk):
        '''Редактирует существующую запись.'''
        try:
            note = Note.objects.get(id=pk)
            if note.user != request.user:
                return Response({"error": "Недоступно редактирование чужой заметки"}, status=403)
            else:
                title = request.data.get('title')
                text = request.data.get('text')
                note.title = title
                note.text = text
                note.fixe_note()
                serializer = NotesSerializer(data={'title': note.title, 'text': note.text})
                return Response({"Заметка отредактирована"}, status=200)
        except Note.DoesNotExist:
            return Response({"error": "Заметка не найдена"}, status=404)

    def delete(self, request, pk):
        '''Удаляет существующую запись.'''
        try:
            note = Note.objects.get(id=pk)
            if note.user != request.user:
                return Response({"error": "Недоступно удаление чужой заметки"}, status=403)
            else:
                note.delete()
                return Response({"Заметка удалена"}, status=204)
        except Note.DoesNotExist:
            return Response({"error": "Заметка не найдена"}, status=404)



def index(request):
    '''Домашняя страница.'''
    return render(request, 'notes_app/index.html')


@login_required()
def notes(request):
    '''Страница со всеми заметками.'''
    notes = Note.objects.filter(user=request.user).order_by('-date_add')
    context = {'notes': notes}
    return render(request, 'notes_app/notes.html', context)


@login_required()
def note(request, note_id: int):
    '''Выводит отдельную заметку.'''
    note = Note.objects.get(id=note_id)
    if note.user != request.user:
        return render(request, 'notes_app/error.html')
    context = {'note': note}
    return render(request, 'notes_app/note.html', context)


@login_required()
def new_note(request):
    '''Создает новую заметку.'''
    if request.method != 'POST':
        form = NoteForm()
    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.fixe_note()
            new_note.save()
            return redirect('notes_app:notes')
    context = {'form': form}
    return render(request, 'notes_app/new_note.html', context)


@login_required()
def edit_note(request, note_id: int):
    '''Редактирует существующую запись.'''
    note = Note.objects.get(id=note_id)
    if request.method != 'POST':
        form = NoteForm(instance=note)
    else:
        form = NoteForm(instance=note, data=request.POST)
        if form.is_valid():
            note.fixe_note()
            return redirect('notes_app:note', note_id=note.id)
    context = {'note': note, 'form': form}
    return render(request, 'notes_app/edit_note.html', context)


@login_required()
def delete_note(request, note_id: int):
    '''Удаляет существующую запись.'''
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('notes_app:notes')
