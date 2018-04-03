#from django.shortcuts import render
from django.views.generic.base import TemplateView

class DeveloperView(TemplateView):
    template_name = 'developer/index.html'
    
class AboutView(TemplateView):
    template_name = 'developer/about.html'
    
class SampleView(TemplateView):
    template_name = 'developer/post.html'
    
class ContactView(TemplateView):
    template_name = 'developer/contact.html'

    

