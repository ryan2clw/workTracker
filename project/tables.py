import django_tables2 as tables
from invoice.models import Project
from django.contrib.auth.models import User

class ProjectTable(tables.Table):
    
    class Meta:
        model = Project
        fields = ('name', 'members')

class UserTable(tables.Table):

    class Meta:
        model = User
        fields = ('username',)
