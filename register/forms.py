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

class TimeTableForm(forms.ModelForm):
    class Meta():
        model = TimeTable
        fields = ('day','class_name','start_time','end_time',)

class AutomateForm(forms.ModelForm):
    msteamgmailid = forms.CharField(max_length = 50,label="MS teams Email:",widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    msteampassword =  forms.CharField(label="MS Teams Password:", widget=forms.PasswordInput(attrs={'required':'true'}))
    msteamorganisationname = forms.CharField(max_length = 50,label="Organization Name:",widget=forms.TextInput(attrs={'placeholder': 'Enter Organization Name:'}))
    discordwebhooklink = forms.CharField(max_length = 1000,label="Discord Webhook Link:",widget=forms.TextInput(attrs={'placeholder': 'Enter Discord Webhook Link:'}))
    class Meta():
        model = AutomateRegister
        fields = ('msteamgmailid','msteampassword','msteamorganisationname','discordwebhooklink',)

