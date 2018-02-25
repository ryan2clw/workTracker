from django.urls import path
from clockin.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
]
