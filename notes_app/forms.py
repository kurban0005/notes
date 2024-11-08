from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text']
        labels = {'title':'', 'text':''}
        widgets = {'text': forms.Textarea(attrs={'cols': 60})}