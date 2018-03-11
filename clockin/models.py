from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import time
import logging
import pytz
import datetime
log = logging.getLogger("workTracker")

class IntervalWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True)
   
    def timeApart(self):
        # Returns 2 decimal delta of time worked
        if self.finished:
            finish = time.mktime(self.finished.timetuple())
            start = time.mktime(self.started.timetuple())
            return "{0:.2f}".format((finish - start)/3600)
        return 0        
       
    def isToday(self):
        if self.started.astimezone(pytz.timezone('US/Eastern')).date() == timezone.now().astimezone(pytz.timezone('US/Eastern')).date():
            return True
        return False
        
    def localTimeStarted(self):
        if True:
            return self.started.astimezone(pytz.timezone('US/Eastern')).strftime("%I:%M:%S %p")
        
    def localTimeFinished(self):
        if True:
            return self.finished.astimezone(pytz.timezone('US/Eastern')).strftime("%I:%M:%S %p")
        
    def __str__(self):
        # Shows name, start and end time for admin
        localDateTimeStart = self.started.astimezone(pytz.timezone('US/Eastern'))
        localDateTimeEnd = ""
        if self.finished:
            localDateTimeEnd += str(self.finished.astimezone(pytz.timezone('US/Eastern')).time())
        else:
            localDateTimeEnd += "active"
        return (self.user.first_name + ": " + str(localDateTimeStart)[:-6] + " - " + localDateTimeEnd)

