from django.db import models
from django.contrib.auth.models import User
import time


class IntervalWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    comments = models.TextField(null=True)
   
    def secondsApart(self):
        # Return some calculated value based on the entry
        if started and finished:
            finish = time.mktime(finished.timetuple())
            start = time.mktime(started.timetuple())
            return finish - start
        return 0
