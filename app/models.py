from django.db import models


# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    grade = models.IntegerField()
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


