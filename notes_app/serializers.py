from rest_framework import serializers
from .models import Note


class NotesSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
