from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User as UserProfile

from .models import *


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        tutor = Role.objects.values('tutor')
        tutee = Role.objects.values('tutee')
        istutor = 0
        for i in range(len(tutor)):
            if tutor[i]['tutor'] == username:
                istutor += 1

        # If the person is a tutee // get a list of tutors and info
        if istutor == 0:
            #list of tutor names
            listoftutors = [0] * len(tutor)
            listofspecialties = [0] * len(tutor)
            tutor = Role.objects.values('tutor')
            for i in range(len(tutor)):
                if tutor[i]['tutor'] != None:
                    listoftutors[i] = tutor[i]['tutor']
                else:
                    listoftutors[i] = 0
            for i in range(len(listoftutors)):
                if listoftutors[i] != 0:
                    listofspecialties[i] = "idk"
                else:
                    listofspecialties[i] = 0
            role = 'Find tutors'
            return render(request, "project/index.html",{
                "role": role,
                "listoftutors": listoftutors,
                "listofspecialties": listofspecialties
            })
        # If the person is a tutor
        elif istutor > 0:
            listoftutees = [0] * len(tutee)
            tutee = Role.objects.values('tutee')
            for i in range(len(tutee)):
                if tutee[i]['tutee'] != None:
                    listoftutees[i] = tutee[i]['tutee']
                else:
                    listoftutees[i] = 0
            role = 'Find tutees'
            return render(request, "project/index.html", {
                "role": role,
                "listoftutees": listoftutees
            })
    return render(request, "project/index.html")

def tutorrequest(request,tutor):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        dates = request.POST['dates']
        tutee = request.POST['tutee']
        tutor = request.POST['tutor']
        f = Requesttutor(subject = subject, message = message, dates = dates, tutee = tutee, tutor = tutor)
        f.save()
        return HttpResponseRedirect(reverse("lifehack:index"))
    return render(request, "project/tutorrequest.html",{
        "tutor": tutor,
    })

def accept(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        dates = request.POST['dates']
        tutee = request.POST['tutee']
        tutor = request.POST['tutor']
        f = Requesttutor.objects.filter(dates = dates, message = message, subject = subject, tutee = tutee, tutor = tutor).first()
        f.delete()
        g = Accept(dates = dates, message = message, subject = subject, tutee = tutee, tutor = tutor)
        g.save()
        return render(request, "project/classroom.html", {
                    "details": g
                })

def profile(request,name):
    if request.user.is_authenticated:
        username = request.user.username
        tutor = Role.objects.values('tutor')
        tutee = Role.objects.values('tutee')
        istutor = 0
        for i in range(len(tutor)):
            if tutor[i]['tutor'] == username:
                istutor += 1

        # If the person is a tutor // get a list of requests
        if istutor > 0:
            requests = Requesttutor.objects.filter(tutor = username)
            accepts = Accept.objects.filter(tutor = username)
            return render(request, "project/profile.html", {
                "name": name,
                "requests": requests,
                "accepts": accepts,
            })
        return render(request, "project/profile.html", {
                "name": name
            })
    return render(request, "project/profile.html", {
        "name": name
    })

def classroom(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        dates = request.POST['dates']
        tutee = request.POST['tutee']
        tutor = request.POST['tutor']
        g = Accept(dates = dates, message = message, subject = subject, tutee = tutee, tutor = tutor)
        return render(request, "project/classroom.html", {
                    "details": g
                })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("lifehack:index"))
        else:
            return render(request, "project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("lifehack:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        
            
        # Ensure password matches confirmation
        password = request.POST["password"]
        
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "project/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "project/register.html", {
                "message": "Username already taken."
            })
        if request.POST.get('tutor'):
            f = Role(tutor = username)
            f.save()
        else:
            f = Role(tutee = username)
            f.save()
        login(request, user)
        return HttpResponseRedirect(reverse("lifehack:index"))
    else:
        return render(request, "project/register.html")
