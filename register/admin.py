from django.contrib import admin
from . models import Student, TimeTable, AutomateRegister

# Register your models here.

admin.site.register(Student)
admin.site.register(TimeTable)
admin.site.register(AutomateRegister)
