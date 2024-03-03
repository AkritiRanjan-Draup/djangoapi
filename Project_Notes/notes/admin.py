from django.contrib import admin
from .models import Note, CustomUser, Folder


# Register your models here.
admin.site.register(Note)
admin.site.register(CustomUser)
admin.site.register(Folder)