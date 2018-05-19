import django_tables2 as tables
from invoice.models import Project

class ProjectTable(tables.Table):

	#myMembers = tables.Column(accessor='timeApart', verbose_name='Members')
    
    class Meta:
        model = Project
        fields = ('name', 'members')
