from django.db import models
from django.contrib.auth.models import User


class IntervalWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    comments = models.TextField(null=True)
   
    
