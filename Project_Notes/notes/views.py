from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from .models import Note, Folder
from .serializers import NoteSerializer, FolderSerializer
from .utilities import execute_query
from .query import get_folders, get_folder_of_id, get_notes_of_folder, get_note_of_id


@api_view(['GET'])
def note_list(request):
    """Parameters:
        - request (HttpRequest): Object containing the request data.
    Returns:
        - Response (HttpResponse): Object containing the serialized data of notes.
    Processing Logic:
        - Fetches all notes if user is a superuser.
        - Fetches notes associated with authenticated user if not a superuser.
        - Serializes the notes and returns the data."""
    if request.user.is_superuser:
        # If the user is a superuser, fetch all notes
        notes = Note.objects.all()

    else:
        # If the user is not a superuser, fetch notes associated with the authenticated user
        notes = Note.objects.filter(user=request.user)

    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


class note_detail(APIView):
    def get_object(self, pk):
        """"Returns the Note object with the given primary key if it exists, otherwise raises a NotFound error."
        Parameters:
            - pk (int): The primary key of the Note object to be retrieved.
        Returns:
            - Note: The Note object with the given primary key.
        Processing Logic:
            - Retrieve Note object by primary key.
            - Check if user is authorized.
            - If Note does not exist, raise error."""
        try:
            return Note.objects.get(pk=pk, user=self.request.user)
        except Note.DoesNotExist:
            raise NotFound("Note not found.")

    def get(self, request, pk):
        """Gets a note of a specific user.
        Parameters:
            - request (HttpRequest): The HTTP request.
            - pk (int): The ID of the note.
        Returns:
            - Response: The note of the specific user.
        Processing Logic:
            - Get user ID from request.
            - Format query to get note of specific user.
            - Execute query.
            - If no result, raise NotFound error.
            - Return response with result."""
        user_id = request.user.id
        query = get_note_of_id.format(note_id=pk, user_id=user_id)
        result = execute_query(query)
        if not result:
            raise NotFound("Note not found.")
        return Response(result)

    def post(self, request):
        """Function:
            Creates a new note for the authenticated user.
        Parameters:
            - request (Request): The HTTP request sent by the user.
        Returns:
            - Response: The serialized data of the newly created note.
            - status (int): The HTTP status code indicating the success or failure of the request.
        Processing Logic:
            - Add the authenticated user's ID to the request data.
            - Validate the request data using the NoteSerializer.
            - If valid, save the data and return a success response.
            - If invalid, return an error response with the validation errors."""
        request.data.update({"user": request.user.id})
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Updates a note and returns the updated note.
        Parameters:
            - request (Request): The HTTP request.
            - pk (int): The primary key of the note to be updated.
        Returns:
            - NoteSerializer: The updated note.
        Processing Logic:
            - Get note from primary key.
            - Validate serializer.
            - Save updated note.
            - Return updated note or errors."""
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Deletes a note and returns a success message.
        Parameters:
            - pk (int): The primary key of the note to be deleted.
        Returns:
            - Response: A success message indicating the note was deleted successfully.
        Processing Logic:
            - Get note by primary key.
            - Delete note.
            - Return success message."""
        note = self.get_object(pk)
        note.delete()
        return Response({"message": "Note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def folder_list(request):
    """Returns:
        - Response: List of folders for user.
    Processing Logic:
        - Get user id from request.
        - Get list of folders from database.
        - Raise error if no folders found.
        - Return list of folders."""
    user_id = request.user.id
    query = get_folders.format(user_id=user_id)
    result = execute_query(query)
    if not result:
        raise NotFound("Folder not found.")
    return Response(result)


class folder_detail(APIView):

    def get_object(self, folder_id):
        """Get folder object by folder ID.
        Parameters:
            - folder_id (int): ID of the folder to retrieve.
        Returns:
            - Folder object: The folder object with the specified ID.
        Processing Logic:
            - Get folder object by ID.
            - Raise error if folder does not exist."""
        try:
            return Folder.objects.get(id=folder_id, user=self.request.user)
        except Folder.DoesNotExist:
            raise NotFound("Folder not found.")

    def get(self, request, folder_id):
        """Get folder from database by folder ID.
        Parameters:
            - request (HttpRequest): Request object.
            - folder_id (int): ID of the folder to retrieve.
        Returns:
            - Response: Folder information.
        Processing Logic:
            - Retrieve folder from database.
            - Check if folder exists.
            - Return folder information."""
        user_id = request.user.id
        query = get_folder_of_id.format(user_id=user_id, folder_id=folder_id)
        result = execute_query(query)
        if not result:
            raise NotFound("Folder not found.")
        return Response(result)

    def post(self, request):
        """Adds a new folder to the database.
        Parameters:
            - request (HttpRequest): The request object containing the data for the new folder.
        Returns:
            - Response: The response object containing the data for the newly created folder.
        Processing Logic:
            - Adds user id to request data.
            - Validates serializer.
            - Saves serializer data.
            - Returns appropriate response."""
        request.data.update({"user": request.user.id})
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, folder_id):
        """Updates a folder with new data.
        Parameters:
            - request (Request): HTTP request.
            - folder_id (int): ID of the folder to be updated.
        Returns:
            - Response: Updated folder data.
        Processing Logic:
            - Get folder by ID.
            - Serialize new data.
            - Save changes.
            - Return updated folder data."""
        folder = self.get_object(folder_id)
        serializer = FolderSerializer(folder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, folder_id):
        """Deletes a folder and returns a success message.
        Parameters:
            - request (HttpRequest): HTTP request object.
            - folder_id (int): ID of the folder to be deleted.
        Returns:
            - Response: Response object with a success message.
        Processing Logic:
            - Get folder object by ID.
            - Delete folder object.
            - Return response with success message."""
        folder = self.get_object(folder_id)
        folder.delete()
        return Response({"message": "Folder deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def folder_note_list(request, folder_id):
    """This function retrieves a list of notes and their associated folder data for a given folder ID. 
    Parameters:
        - request (Request): The request object.
        - folder_id (int): The ID of the folder to retrieve notes from.
    Returns:
        - Response: A response object containing a list of notes and their associated folder data.
    Processing Logic:
        - Retrieve the folder with the given ID.
        - Execute a query to retrieve notes associated with the folder.
        - Create a dictionary containing the folder's name, creation date, and update date.
        - Create a response object containing the notes and folder data."""
    folders = Folder.objects.filter(id=folder_id, user=request.user)
    if not folders:
        raise NotFound("Folder not found.")

    folder = folders.first()

    query = get_notes_of_folder.format(folder_id=folder_id)
    result = execute_query(query)

    folder_data = {
        "name": folder.name,
        "created_at": folder.created_at,
        "updated_at": folder.updated_at
    }

    response_data = {
        "notes_data": result,
        "folder_data": folder_data
    }
    return Response(response_data)

