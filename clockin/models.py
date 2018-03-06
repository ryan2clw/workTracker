from django.db import models
from django.contrib.auth.models import User
import time
import logging
import pytz
import datetime
log = logging.getLogger("workTracker")

class IntervalWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # created = models.DateTimeField(null=True, blank=True)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True)
   
    def timeApart(self):
        # Returns 2 decimal delta of time worked
        if self.started and self.finished:
            finish = time.mktime(self.finished.timetuple())
            start = time.mktime(self.started.timetuple())
            return "{0:.2f}".format((finish - start)/3600)
        return 0
        
    def localTimeStarted(self):
        #utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        #return self.started.astimezone(pytz.timezone('US/Eastern'))
        #est = pytz.timezone('US/Eastern')
        return self.started.astimezone(pytz.timezone('US/Eastern'))
        #localToday = datetime.date.fromtimestamp(time.mktime(est_now.timetuple()))
        
    def __str__(self):
        # Shows name, start and end time for admin
        localDateTimeStart = self.started.astimezone(pytz.timezone('US/Eastern'))
        localDateTimeEnd = ""
        if self.finished:
            localDateTimeEnd += str(self.finished.astimezone(pytz.timezone('US/Eastern')).time())
        else:
            localDateTimeEnd += "active"
        return (self.user.first_name + ": " + str(localDateTimeStart)[:-6] + " - " + localDateTimeEnd)

