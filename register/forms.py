from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from . models import Student, TimeTable, AutomateRegister

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required':'true'}))

    class Meta():
        model = User
        fields = ('username', 'email', 'password',)

class StudentForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('name', 'college', 'usn_no',)
