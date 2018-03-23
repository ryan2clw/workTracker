import django_tables2 as tables
from clockin.models import IntervalWork

class IntervalTable(tables.Table):
    startedFormatted = tables.Column(accessor='localTimeStarted', verbose_name='Started')
    finishedFormatted = tables.Column(accessor='localTimeFinished', verbose_name='Finished')
    myHours = tables.Column(accessor='timeApart', verbose_name='Hours')
    
    class Meta:
        model = IntervalWork
        exclude = ('id', 'user', 'started', 'finished', 'project', 'paid')
        sequence = ('startedFormatted', 'finishedFormatted', 'myHours', 'comments')
        attrs = {"class" : "table-striped table-bordered"}
        empty_text = "There are no hours logged today."
     
'''

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)'''   
        
