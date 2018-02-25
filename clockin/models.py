from django.db import models
from django.contrib.auth.models import User

class IntervalWork:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.DateTimeField()
    finished = models.DateTimeField()
    comments = models.TextField()
