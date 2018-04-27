import logging
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from pytz import timezone as pytzTZ
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework import permissions
from django_tables2 import RequestConfig
from clockin.models import IntervalWork
from clockin.serializers import IntervalWorkSerializer
from clockin.forms import ClockinForm
from clockin.tables import IntervalTable
from invoice.models import Project
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

log = logging.getLogger("workTracker")

# Clockin View

class IndexView(LoginRequiredMixin, ListView):
    model = IntervalWork
    template_name = 'clockin/index.html'
    context_object_name = 'IntervalWork' # the variable name of the object in the template
    ordering = ['id']
    myProjects = None
    currentProject = None
    def get_queryset(self):
        self.myProjects = Project.objects.all()
        for project in self.myProjects:
            IntervalWorks = IntervalWork.objects.filter(user_id=self.request.user.id, project_id=project.id, 
            started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).values()
            log.debug("startedGTE: " + str(timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)))
            for work in IntervalWorks:
                if not work["finished"]:
                    self.currentProject = project.name
        if self.currentProject:
            myProject = Project.objects.get(name=self.currentProject)
            return IntervalWork.objects.filter(user_id=self.request.user.id, project_id=myProject.id,
                started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).order_by('started')
        else:
            try:
                myProject = Project.objects.get(name=self.request.GET["project"])
                return IntervalWork.objects.filter(user_id=self.request.user.id, project_id=myProject.id,
                    started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).order_by('started')
            except:
                return IntervalWork.objects.none()

    def get_context_data(self, **kwargs): 
        # Initializes the state of the view
        context = super(IndexView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['clockedIn'] = "Not Clocked In"
        context['projects'] = self.myProjects
        context['myForm'] = ClockinForm()
        context['currentProject'] = self.currentProject
        try:
            myHours = self.object_list
            context['myHours'] = myHours
            if not myHours.last().finished:
                context['clockedIn'] = "Clocked In"
            table = IntervalTable(myHours) # gotta love list comprehensions 
            context['totalHours'] = format(sum([float(interval.timeApart()) for interval in myHours]), '.2f')
            RequestConfig(self.request, paginate=False).configure(table)
            context['table'] = table
        except:
            pass
        return context
        
    def get(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="developer").exists():
            return HttpResponseRedirect(reverse('menu') + "?developer=none")
        return super(IndexView, self).get(request, *args, **kwargs)

# REST ENDPOINTS

class WorkUpdate(UpdateAPIView):

    queryset = IntervalWork.objects.all() #
    serializer_class = IntervalWorkSerializer
    
    def get_queryset(self):
        return IntervalWork.objects.filter(user_id=self.request.user.id).order_by('started')
    
class WorkCreate(CreateAPIView):
    queryset = IntervalWork.objects.all()
    serializer_class = IntervalWorkSerializer

class WorkList(ListAPIView):

    serializer_class = IntervalWorkSerializer
    model = IntervalWork
    context_object_name = 'IntervalWork' # the variable name of the object in the template
    ordering = ['id']
    myProjects = None
    currentProject = None
    permission_classes = [ permissions.IsAuthenticated, ]

    def get_queryset(self):
        # this routine checks for open projects first, then if none are open, 
        # retrieves GET['project']'s objects if they're from today, else none
        self.myProjects = Project.objects.all()
        for project in self.myProjects:
            IntervalWorks = IntervalWork.objects.filter(user_id=self.request.user.id, project_id=project.id, 
            started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).values()
            for work in IntervalWorks:
                if not work["finished"]:
                    self.currentProject = project.name
        if self.currentProject:
            myProject = Project.objects.get(name=self.currentProject)
            return IntervalWork.objects.filter(user_id=self.request.user.id, project_id=myProject.id,
                started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).order_by('started')
        else:
            try:
                myProject = Project.objects.get(name=self.request.GET["project"])
                return IntervalWork.objects.filter(user_id=self.request.user.id, project_id=myProject.id,
                    started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).order_by('started')
            except:
                return IntervalWork.objects.none()
    def get(self, request, *args, **kwargs):
        return super(WorkList, self).get(request, *args, **kwargs)
