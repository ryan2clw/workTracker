from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework import permissions
from clockin.serializers import ProjectSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from django_tables2 import RequestConfig
from invoice.models import Project
from project.forms import UserAddForm
from project.tables import ProjectTable

class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project.html'

    def get_context_data(self, **kwargs): 
        # Initializes the state of the view
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['myForm'] = UserAddForm()
        context['user_email'] = self.request.user.username
        table = ProjectTable(self.object_list)
        RequestConfig(self.request, paginate=False).configure(table)
        context['table'] = table
        return context

    def get_queryset(self):
        return Project.objects.filter(members__id=self.request.user.id)

    def form_valid(self, form):
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post(url, values)
        ''' End reCAPTCHA validation '''
        if response.ok:
            super(ProjectView, self).form_valid(form)
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.') 

class ProjectList(ListAPIView):

    serializer_class = ProjectSerializer
    model = Project
    permission_classes = [ permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = User.objects.get(username=self.request.GET["username"])
        return Project.objects.filter(members__id=user.id)


class ProjectCreate(CreateAPIView):
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

class UserUpdate(UpdateAPIView):

    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()
'''
     UPDATE lets you set the project list directly

     use the serializer class 

    def update(self):
        myProjects = Project.objects.filter(members__id=self.request.user.id)'''



