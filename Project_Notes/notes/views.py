from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def note_list(request):
    """Parameters:
        - request (HttpRequest): Object containing the request data.
    Returns:
        - Response (HttpResponse): Object containing the serialized data of notes.
    Processing Logic:
        - Fetches all notes if user is a superuser.
        - Fetches notes associated with authenticated user if not a superuser.
        - Serializes the notes and returns the data."""
    if request.method == 'GET':
        if request.user.is_superuser:
            # If the user is a superuser, fetch all notes
            notes = Note.objects.all()
        else:
            # If the user is not a superuser, fetch notes associated with the authenticated user
            notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail(request, pk):
    """This function allows for GET, PUT, and DELETE requests for a specific note, given its primary key (pk). Only authenticated users can access this function. If the note does not exist, a 404 error is returned. If the user who created the note is not the one accessing it, a 403 error is returned. The function returns the note's data for a GET request, updates the note's data for a PUT request, and deletes the note for a DELETE request. 
    Parameters:
        - request (HttpRequest): The request object.
        - pk (int): The primary key of the note to be accessed.
    Returns:
        - Response (HttpResponse): The response object containing the note's data for a GET request, or a success/error message for a PUT or DELETE request. 
    Processing Logic:
        - Ensure that only authenticated users can access the function.
        - Check if the note exists, and return a 404 error if it does not.
        - Check if the user accessing the note is the one who created it, and return a 403 error if not.
        - For a GET request, return the note's data using the NoteSerializer.
        - For a PUT request, update the note's data using the NoteSerializer, and return the updated data.
        - For a DELETE request, delete the note and return a success message."""
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Ensure that only the user who created the note can access it
    if note.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

