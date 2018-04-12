from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import UpdateAPIView, CreateAPIView
from django_tables2 import RequestConfig
from clockin.models import IntervalWork
from clockin.serializers import IntervalWorkSerializer
from django.utils import timezone
from pytz import timezone as pytzTZ
from clockin.forms import ClockinForm
from clockin.tables import IntervalTable
from invoice.models import Project
import logging

log = logging.getLogger("workTracker")
        
# Clockin View

class IndexView(LoginRequiredMixin, ListView):
    model = IntervalWork
    template_name = 'clockin/index.html'
    context_object_name = 'interval' # the variable name of the object in the template
    ordering = ['id']
    myProjects = None
    
    def get_queryset(self):
        self.myProjects = Project.objects.all()
        log.debug(self.myProjects)
        try:
            #log.debug(self.request.GET["project"]);
            myProject = Project.objects.get(name=self.request.GET["project"])
            log.debug(myProject)
            return IntervalWork.objects.filter(user_id=self.request.user.id, project_id=myProject.id,
                started__gte=timezone.now().astimezone(pytzTZ('US/Eastern')).replace(hour=0, minute=0, second=0)).order_by('started')
        except:
            return IntervalWork.objects.none()

    def get_context_data(self, **kwargs): 
        # Initializes the state of the view
        context = super(IndexView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['clockedIn'] = "Clocked In"
        context['projects'] = self.myProjects
        myHours = self.object_list
        context['myHours'] = myHours
        if not myHours or myHours.last().finished:
            context['clockedIn'] = "Not Clocked In"
        table = IntervalTable(myHours) # gotta love list comprehensions 
        context['totalHours'] = format(sum([float(interval.timeApart()) for interval in myHours]), '.2f')
        RequestConfig(self.request, paginate=False).configure(table)
        context['table'] = table
        context['myForm'] = ClockinForm()
        return context

# REST ENDPOINTS

class WorkUpdate(UpdateAPIView):
    queryset = IntervalWork.objects.all()
    #project = Project.objects.get(name="Demo")
    serializer_class = IntervalWorkSerializer
    
    def get_queryset(self):
        return IntervalWork.objects.filter(user_id=self.request.user.id).order_by('started')
    
class WorkCreate(CreateAPIView):
    queryset = IntervalWork.objects.all()
    serializer_class = IntervalWorkSerializer
