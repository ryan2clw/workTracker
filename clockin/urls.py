from django.urls import path
from clockin.views import IndexView, WorkCreate, WorkUpdate, WorkList, ProjectList
from django.http import HttpResponse

urlpatterns = [
    path('', IndexView.as_view(), name='clockin'),
    path('new/', WorkCreate.as_view(), name='work_new'),
    path('update/<pk>/', WorkUpdate.as_view(), name='work_update'),
    path('list/', WorkList.as_view(), name='work_list'),
    path('projects/', ProjectList.as_view(), name='project_list'),
] 
