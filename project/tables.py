import django_tables2 as tables
from invoice.models import Project
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class ProjectTable(tables.Table):
    
    class Meta:
        model = Project
        fields = ('name', 'members')

class UserTable(tables.Table):

    buttons = tables.LinkColumn(empty_values=(), verbose_name='Action')

    class Meta:
        model = User
        fields = ('username','buttons')

    def render_buttons(self, record):
        return mark_safe('<button onclick="deleteUser()" class="btn-sm btn-danger">Delete</button>')