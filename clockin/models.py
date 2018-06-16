from django.db import models
from django.contrib.auth.models import User
from invoice.models import Project
from django.utils import timezone
import time
import logging
import pytz
import datetime
log = logging.getLogger("workTracker")

class Bill(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return (self.project.name + '\n  pay rate: ' + str(self.pay_rate) + '\n  tax: ' + str(self.tax))

class IntervalWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True)
    paid = models.BooleanField(default=False)   
   
    def timeApart(self):
        # Returns 2 decimal delta of time worked
        if self.finished:
            finish = time.mktime(self.finished.timetuple())
            start = time.mktime(self.started.timetuple())
            return "{0:.2f}".format((finish - start)/3600)
        return 0        
        
    def localTimeStarted(self):
        return self.started.astimezone(pytz.timezone('US/Eastern')).strftime("%I:%M:%S %p")
        
    def localTimeFinished(self):
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

