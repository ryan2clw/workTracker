from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from invoice.models import Project # TO DO: ADD MODEL AND TEMPLATE
from clockin.serializers import ProjectSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView

class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project.html'

    def get_context_data(self, **kwargs): 
        # Initializes the state of the view
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        print(context['first_name'])
        return context

class ProjectCreate(CreateAPIView):
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

class UserUpdate(UpdateAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

'''
     UPDATE lets you set the project list directly

     use the serializer class 

    def update(self):
        myProjects = Project.objects.filter(members__id=self.request.user.id)'''




