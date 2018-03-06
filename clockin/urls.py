from django.urls import path
from clockin.views import IndexView, WorkCreate, WorkUpdate
from django.http import HttpResponse

urlpatterns = [
    path('', IndexView.as_view(), name='clockin'),
    path('new/', WorkCreate.as_view(), name='work_new'),
    path('update/<pk>/', WorkUpdate.as_view(), name='work_update'),
] 
