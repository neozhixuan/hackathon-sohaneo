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
    def __str__ (self):
        return f"Tutor: {self.tutor}, Tutee: {self.tutee}, {self.message}"