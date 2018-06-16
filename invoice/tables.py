import django_tables2 as tables
from clockin.models import IntervalWork

class BillingTable(tables.Table):
    #startedFormatted = tables.Column(accessor='localTimeStarted', verbose_name='Started')
    #finishedFormatted = tables.Column(accessor='localTimeFinished', verbose_name='Finished')
    myHours = tables.Column(accessor='timeApart', verbose_name='Hours')
    
    class Meta:
        model = IntervalWork
        exclude = ('id', 'user', 'project', 'paid','bill') #'started', 'finished', 
        sequence = ('started', 'finished', 'myHours', 'comments')
        attrs = {"class" : "table-striped table-bordered"}
        empty_text = "Paid in full."
