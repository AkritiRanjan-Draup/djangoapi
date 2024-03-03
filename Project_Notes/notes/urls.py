from django.urls import path
from .views import note_list, note_detail, folder_list, folder_detail, folder_note_list

urlpatterns = [
    path('notes/', note_list, name='note-list'),
    path('notes/<int:pk>/', note_detail.as_view(), name='note-detail'),
    path('folders/', folder_list, name='folder-list'),
    path('folders/<int:folder_id>/', folder_detail.as_view(), name='folder-detail'),
    path('folders/<int:folder_id>/notes/', folder_note_list, name='note-list'),
]
