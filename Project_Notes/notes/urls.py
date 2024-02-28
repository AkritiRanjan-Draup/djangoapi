from django.urls import path
from .views import note_list, note_detail

urlpatterns = [
    path('notes/', note_list, name='note-list'),
    path('notes/<int:pk>/', note_detail, name='note-detail'),
]
