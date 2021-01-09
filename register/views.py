from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from . models import Student, TimeTable, AutomateRegister
from . forms import UserForm, StudentForm, TimeTableForm, AutomateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required                   #view required to user to logged in this decorator is used
import auto
from datetime import datetime

# Create your views here.

def index(request):
    return render(request,'index.html')

def autoClazz(request):
    return render(request,'index1.html')

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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)            
            else:
                return HttpResponse('User not active')

        else:
            return HttpResponse('Invalid credentials')
        return HttpResponseRedirect('/')

    else:
        return render(request, 'login.html')

@login_required(login_url = "/login")
def automate(request):
    if TimeTable.objects.filter(user = request.user).exists() and AutomateRegister.objects.filter(user = request.user):
        msteam = get_object_or_404(AutomateRegister, user = request.user)
        email = msteam.msteamgmailid
        password = msteam.msteampassword
        webhooklink = msteam.discordwebhooklink
        orgname = msteam.msteamorganisationname
        day = datetime.today().strftime("%A")
        timetable = TimeTable.objects.filter(user = request.user, day = day)
        auto.bot(email, password, webhooklink, orgname, timetable)
        return HttpResponseRedirect('/')

    elif not (TimeTable.objects.filter(user = request.user).exists() or AutomateRegister.objects.filter(user = request.user).exists()):
        return HttpResponse("Register TimeTable and MicroSoft teams details")
    
    elif not TimeTable.objects.filter(user = request.user).exists():
        return HttpResponse("Register TimeTable")
    
    elif not AutomateRegister.objects.filter(user = request.user).exists():
        return HttpResponse("Register MicroSoft teams details")


@login_required(login_url = "/login")
def autoregister(request):
    user = get_object_or_404(User, username = request.user)
    if request.method == "POST":
        if AutomateRegister.objects.filter(user = request.user).exists():
            instance = get_object_or_404(AutomateRegister, user = request.user)
            autoform = AutomateForm(request.POST, instance = instance)
            if autoform.is_valid():
                automate = autoform.save(commit = False)
                automate.user = user
                automate.save()
            return HttpResponseRedirect('/')
        else:
            autoform = AutomateForm(request.POST)
            if autoform.is_valid():
                automate = autoform.save(commit = False)
                automate.user = user
                automate.save()
            return HttpResponseRedirect('/')

    else:
        if AutomateRegister.objects.filter(user = request.user).exists():
            instance = get_object_or_404(AutomateRegister, user = request.user)
            form = AutomateForm(instance = instance)
            return render(request, 'autoregister.html', {'form': form})
        else:
            form = AutomateForm()
            return render(request, 'autoregister.html', {'form': form})

@login_required(login_url = "/login")
def timetable(request):
    user = get_object_or_404(User, username = request.user)
    if request.method == "POST":
        timetableform = TimeTableForm(request.POST)
        if timetableform.is_valid():
            timetable = timetableform.save(commit = False)
            timetable.user = user
            timetable.save()
            form = TimeTableForm()
            timetabledata = TimeTable.objects.filter(user = request.user)
            return render(request, 'timetableregister.html', {'form': form, 'timetabledata': timetabledata})

    else:
        form = TimeTableForm()
        timetabledata = TimeTable.objects.filter(user = request.user)
        return render(request, 'timetableregister.html', {'form': form, 'timetabledata': timetabledata})

@login_required(login_url = "/login")
def deletettdata(request, id):
    TimeTable.objects.filter(id=id).delete()
    return HttpResponseRedirect('/timetable')

    



