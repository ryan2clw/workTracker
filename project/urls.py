from django.urls import path
from project.views import ProjectView, ProjectCreate, UserUpdate
from django.http import HttpResponse

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('new/', ProjectCreate.as_view(), name='project_new'),
    path('user/<pk>/', UserUpdate.as_view(), name='user_update'),
]
