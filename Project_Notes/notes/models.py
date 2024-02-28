from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    pass


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        """"Returns the title of the object."
        Parameters:
            - None
        Returns:
            - str: The title of the object.
        Processing Logic:
            - Returns the title attribute.
            - No parameters needed.
            - Title is a string.
        """
        return self.title
