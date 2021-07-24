from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Role(models.Model):
    tutor = models.CharField(blank = True, null=True, max_length = 100)
    tutee = models.CharField(blank = True, null=True, max_length = 100)

    def __str__ (self):
        return f"Tutor: {self.tutor}, Tutee: {self.tutee}"

class Requesttutor(models.Model):
    tutor = models.CharField(blank = True, null=True, max_length = 100)
    tutee = models.CharField(blank = True, null=True, max_length = 100)
    subject = models.CharField(blank = True, null=True, max_length = 100)
    message = models.CharField(blank = True, null=True, max_length = 10000)
    dates = models.CharField(blank = True, null=True, max_length = 100)
    def __str__ (self):
        return f"Tutor: {self.tutor}, Tutee: {self.tutee}, {self.message}"

class Accept(models.Model):
    tutor = models.CharField(blank = True, null=True, max_length = 100)
    tutee = models.CharField(blank = True, null=True, max_length = 100)
    subject = models.CharField(blank = True, null=True, max_length = 100)
    message = models.CharField(blank = True, null=True, max_length = 10000)
    dates = models.CharField(blank = True, null=True, max_length = 100)
    encryption = models.CharField(blank = True, null=True, max_length = 100)
    def __str__ (self):
        return f"Tutor: {self.tutor}, Tutee: {self.tutee}, {self.message}"

class Message(models.Model):
    user = models.CharField(blank = True, null=True, max_length = 100)
    tuteebool = models.CharField(blank = True, null=True, max_length = 100)
    message = models.CharField(blank = True, null=True, max_length = 10000)
    encryption = models.CharField(blank = True, null=True, max_length = 100)
    def __str__ (self):
        return f"Message by {self.user}: {self.message}"

class Polls(models.Model):
    encryption = models.CharField(blank = True, null=True, max_length = 100)
    user = models.CharField(blank = True, null=True, max_length = 100)
    question = models.CharField(blank = True, null=True, max_length = 10000)
    answer = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer1 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer2 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer3 = models.CharField(blank = True, null=True, max_length = 10000)
    question2 = models.CharField(blank = True, null=True, max_length = 10000)
    answer2 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer4 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer5 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer6 = models.CharField(blank = True, null=True, max_length = 10000)
    question3 = models.CharField(blank = True, null=True, max_length = 10000)
    answer3 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer7 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer8 = models.CharField(blank = True, null=True, max_length = 10000)
    fakeanswer9 = models.CharField(blank = True, null=True, max_length = 10000)
    def __str__ (self):
        return f"{self.question}: {self.answer}"

class Canteen(models.Model):
    message = models.CharField(blank = True, null=True, max_length = 10000)
    user = models.CharField(blank = True, null=True, max_length = 100)
    likes = models.IntegerField(blank = True, null=True)