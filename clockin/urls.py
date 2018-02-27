from django.urls import path
from clockin.views import IndexView, WorkCreate, WorkUpdate
#from clockin import views
#IndexView, workCreate, workUpdate

urlpatterns = [
    path('', IndexView.as_view(), name='clockin'),
    #path('new', IndexView.post, name='work_new')
    path('new/', WorkCreate.as_view(), name='work_new'),
    path('started/<pk>/', WorkUpdate.as_view(), name='started'),
    #path('update/<pk>/', WorkUpdate.as_view(), name="work_update"),
    #path('edit/<pk>/', views.workUpdate, name='work_edit'),
]
