from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
class Student(models.Model):
    name = models.CharField(max_length=25)
    usn = models.CharField(max_length=10,primary_key=True)
    address = models.TextField()
    sem = models.IntegerField(default=1)
    classrm = models.ForeignKey('Classroom',null=True,blank=True,\
        on_delete=models.CASCADE)'''

class Faculty(models.Model):
    name = models.CharField(max_length=25)
    ssn = models.CharField(max_length=10,primary_key=True)
    address = models.TextField()
    dept = models.CharField(max_length=10)

class Course(models.Model):
    name = models.CharField(max_length=20)
    sem = models.IntegerField()

class Classroom(models.Model):
    name = models.CharField(max_length=10)
    dept = models.CharField(max_length=10)
    sem = models.IntegerField(default=1)
    course = models.ManyToManyField(Course)


days = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thurday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 20)
    college = models.CharField(max_length = 50)
    usn_no = models.CharField(max_length = 20)

class TimeTable(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    day = models.CharField(max_length = 20, choices = days)
    class_name = models.CharField(max_length = 20)
    start_time = models.CharField(max_length = 20)
    end_time = models.CharField(max_length = 20)

class AutomateRegister(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    msteamgmailid = models.EmailField()
    msteampassword = models.CharField(max_length = 50)
    msteamorganisationname = models.CharField(max_length = 50)
    discordwebhooklink = models.CharField(max_length = 500)

