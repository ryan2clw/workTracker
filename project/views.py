from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework import permissions
from clockin.serializers import ProjectSerializer, UserSerializer, ProjectMemberSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from django_tables2 import RequestConfig
from invoice.models import Project
from project.forms import UserAddForm, InviteForm, UserDeleteForm
from project.tables import ProjectTable, UserTable

class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project.html'

    def get_context_data(self, **kwargs): 
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['myForm'] = UserAddForm()
        context['user_email'] = self.request.user.username        
        context['hasProjects'] = "false"
        deleteForm = UserDeleteForm()
        context['deleteForm'] = deleteForm
        if len(self.object_list) > 0:
            context['hasProjects'] = "true"
        try:
        	# PARAMETER 'PROJECT' HELPS FORM USER LIST (USER MODE)
            myProject = Project.objects.filter(name=self.request.GET['project'])[0]
            context['hasProjects'] = "true"
            myUsers = myProject.members.all()
            context['currentID'] = myProject.id
            context['currentProject'] = myProject.name
            context['inviteForm'] = InviteForm()
            table = UserTable(myUsers)
            context['table'] = table
        except:
        	# NO PARAMETER SPECIFIED IS LIKE PROJECT MODE
            table = ProjectTable(self.object_list)
            table.requestor = self.request.user.username
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

class ProjectMemberList(ListAPIView):

    serializer_class = ProjectMemberSerializer
    model = Project
    permission_classes = [ permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = User.objects.get(username=self.request.GET["username"])
        return Project.objects.filter(members__id=user.id)

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

class ProjectDelete(DestroyAPIView):

    serializer_class = ProjectSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Project.objects.all()

class UserUpdate(UpdateAPIView):

    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()





