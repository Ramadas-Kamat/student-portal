from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 20)
    college = models.CharField(max_length = 50)
    usn_no = models.CharField(max_length = 20)

class TimeTable(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    day = models.CharField(max_length = 20)
    class_name = models.CharField(max_length = 20)
    start_time = models.CharField(max_length = 20)
    end_time = models.CharField(max_length = 20)

