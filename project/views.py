from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
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
        unique_id = get_random_string(length=15)
        g = Accept(dates = dates, message = message, subject = subject, tutee = tutee, tutor = tutor, encryption = unique_id)
        g.save()
        classroom = Accept.objects.get(encryption = unique_id)
        messages = Message.objects.filter(encryption = unique_id)
        polls = Polls.objects.filter(encryption=unique_id)
        return render(request, "project/classroom.html", {
                    "details": classroom,
                    "messages": messages,
                    "polls": polls
                })

def profile(request,name):
    if request.user.is_authenticated:
        tutor = Role.objects.values('tutor')
        tutee = Role.objects.values('tutee')
        istutor = 0
        for i in range(len(tutor)):
            if tutor[i]['tutor'] == name:
                istutor += 1
        canteenmessages = Canteen.objects.filter(user = name)
        points = 0
        for i in range(len(canteenmessages)):
            points = points + canteenmessages[i].likes
        
        # If the person is a tutor // get a list of requests
        if istutor > 0:
            requests = Requesttutor.objects.filter(tutor = name)
            accepts = Accept.objects.filter(tutor = name)
            return render(request, "project/profile.html", {
                "name": name,
                "requests": requests,
                "accepts": accepts,
                "points": points,
            })
        else:
            accepts = Accept.objects.filter(tutee = name)
            return render(request, "project/profile.html", {
                "name": name,
                "accepts": accepts,
                "points": points,
            })
    canteenmessages = Canteen.objects.filter(user = name)
    points = 0
    for i in range(len(canteenmessages)):
        points = points + int(canteenmessages[i].likes)
    return render(request, "project/profile.html", {
        "name": name,
        "points": points,
    })

def tuteemessage(request):
    if request.method == "POST":
        user = request.POST['user']
        tuteebool = request.POST['tutee']
        message = request.POST['message']
        encryption = request.POST['encryption']
        f = Message(user = user, tuteebool = tuteebool, message = message, encryption = encryption)
        f.save()

        classroom = Accept.objects.get(encryption = encryption)
        messages = Message.objects.filter(encryption = encryption)
        polls = Polls.objects.filter(encryption=encryption)
        return render(request, "project/classroom.html", {
                    "details": classroom,
                    "messages": messages,
                    "polls": polls
                })

def classroom(request):
    if request.method == "POST":
        encryption = request.POST['encryption']
        g = Accept.objects.get(encryption = encryption)

        username = request.user.username
        tutor = Role.objects.values('tutor')
        istutor = 0
        for i in range(len(tutor)):
            if tutor[i]['tutor'] == username:
                istutor += 1

        # If the person is a tutee // get a list of tutors and info
        if istutor == 0:
            tutee = "Yes"
        else:
            tutee = None
        messages = Message.objects.filter(encryption = encryption)
        polls = Polls.objects.filter(encryption=encryption)
        return render(request, "project/classroom.html", {
                    "details": g,
                    "tutee": tutee,
                    "messages": messages,
                    "polls":polls
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

def create(request):
    if request.method == "POST":
        encryption = request.POST['encryption']
        user = request.POST['user']
        question = request.POST['question']
        answer = request.POST['answer']
        fakeanswer1 = request.POST['fakeanswer1']
        fakeanswer2 = request.POST['fakeanswer2']
        fakeanswer3 = request.POST['fakeanswer3']
        question2 = request.POST['question2']
        answer2 = request.POST['answer2']
        fakeanswer4 = request.POST['fakeanswer4']
        fakeanswer5 = request.POST['fakeanswer5']
        fakeanswer6 = request.POST['fakeanswer6']
        question3 = request.POST['question3']
        answer3 = request.POST['answer2']
        fakeanswer7 = request.POST['fakeanswer7']
        fakeanswer8 = request.POST['fakeanswer8']
        fakeanswer9 = request.POST['fakeanswer9']
        f = Polls(encryption=encryption,user=user,question=question,answer=answer,fakeanswer1=fakeanswer1,fakeanswer2=fakeanswer2,fakeanswer3=fakeanswer3,question2=question2,answer2=answer2,fakeanswer4=fakeanswer4,fakeanswer5=fakeanswer5,fakeanswer6=fakeanswer6,question3=question3,answer3=answer3,fakeanswer7=fakeanswer7,fakeanswer8=fakeanswer8,fakeanswer9=fakeanswer9)
        f.save()
        classroom = Accept.objects.get(encryption = encryption)
        messages = Message.objects.filter(encryption = encryption)
        polls = Polls.objects.filter(encryption=encryption)
        return render(request, "project/classroom.html", {
                    "details": classroom,
                    "messages": messages,
                    "polls": polls
                })

def polldesign(request):
    if request.method == "POST":
        encryption = request.POST['encryption']
        user = request.POST['user']
        return render(request, "project/polldesign.html", {
            "encryption": encryption,
            "user": user,
                })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("lifehack:index"))

def canteen(request):
    if request.method == "POST":
        user = request.POST['user']
        message = request.POST['message']
        f = Canteen(user=user,message=message,likes=0)
        f.save()
        messages = Canteen.objects.all()
        return render(request, "project/canteen.html",{
        "messages": messages
        })
    messages = Canteen.objects.all()
    return render(request, "project/canteen.html",{
        "messages": messages
    })

def like(request):
    if request.method == "POST":
        user = request.POST['user']
        message = request.POST['message']
        f = Canteen.objects.filter(user = user, message = message).first()
        likes = f.likes
        likes = likes + 1
        f.likes = likes
        f.save()

        messages = Canteen.objects.all()
        return render(request, "project/canteen.html",{
            "messages": messages
        })

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
