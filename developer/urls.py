from developer.views import DeveloperView, AboutView, SampleView, ContactView
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', DeveloperView.as_view(), name='developer'),
    path('about', AboutView.as_view(), name='about'),
    path('sample', SampleView.as_view(), name='sample'),
    path('contact', ContactView.as_view(), name='contact'),
]
