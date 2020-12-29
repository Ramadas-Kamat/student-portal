from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=25)
    usn = models.CharField(max_length=10,primary_key=True)
    address = models.TextField()
    sem = models.IntegerField(default=1)
    classrm = models.ForeignKey('Classroom',null=True,blank=True,\
        on_delete=models.CASCADE)

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
