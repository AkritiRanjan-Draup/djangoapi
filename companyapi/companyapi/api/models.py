from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
