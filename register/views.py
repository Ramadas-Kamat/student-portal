from django.shortcuts import render
from django.contrib.auth.models import User
from . models import Student, TimeTable, AutomateRegister
from . forms import UserForm, StudentForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required                   #view required to user to logged in this decorator is used


# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        studentform = StudentForm(request.POST)
        if userform.is_valid() and studentform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            student = studentform.save(commit = False)
            student.user = user
            student.save()
        return HttpResponseRedirect('/')
    else:
        userform = UserForm()
        studentform = StudentForm()
        return render(request, 'register.html', {'userform': userform, 'studentform': studentform})

# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)            
#             else:
#                 return HttpResponse('User not active')

#         else:
#             return HttpResponse('Invalid credentials')

#     else:
#         return render(request, 'dbmsA/login.html')

def automate(request):
    return HttpResponseRedirect('/')
