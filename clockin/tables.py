import django_tables2 as tables
from django_tables2.utils import A
from .models import IntervalWork


class IntervalTable(tables.Table):
    #started = tables.LinkColumn('started', args=[A('pk')])
    #ended = tables.LinkColumn('ended', args=[A('pk')])
    #started = tables.DateTimeColumn(format ='h:i:s A')
    started = tables.DateTimeColumn(format ='h:i:s A')
    finished = tables.DateTimeColumn(format ='h:i:s A')
    #startedFormatted = tables.Column(accessor='localTimeStarted', verbose_name='Started')
    my_extra_column = tables.Column(accessor='timeApart', verbose_name='Hours')
    
    class Meta:
        model = IntervalWork
        exclude = ('id', 'user')
        sequence = ('started', 'finished', 'comments', 'my_extra_column')
        attrs = {"class" : "table-striped table-bordered"}
        empty_text = "There are no hours logged today."
