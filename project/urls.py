from django.urls import path
from project.views import ProjectView
from django.http import HttpResponse

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
]
