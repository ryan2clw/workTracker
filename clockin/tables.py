import django_tables2 as tables
from django_tables2.utils import A
from .models import IntervalWork


class IntervalTable(tables.Table):
    started = tables.LinkColumn('started', args=[A('pk')])
    ended = tables.LinkColumn('ended', args=[A('pk')])
    
    class Meta:
        model = IntervalWork
        fields = ( 'created', 'user','started', 'ended','comments',)
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no hours logged today."
