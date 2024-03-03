from rest_framework import serializers
from .models import Note, Folder


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ['id']


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
