from django.contrib import admin
from invoice.models import Project
from clockin.models import Bill

admin.site.register(Project)
admin.site.register(Bill)
