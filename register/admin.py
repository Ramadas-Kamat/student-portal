from django.contrib import admin
from . models import Student, TimeTable, AutomateRegister, Faculty

admin.site.register(Faculty)




admin.site.register(Student)
admin.site.register(TimeTable)
admin.site.register(AutomateRegister)
