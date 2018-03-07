from django.views.generic import TemplateView, ListView, View
#from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import UpdateAPIView, CreateAPIView
from django_tables2 import RequestConfig
from clockin.models import IntervalWork
from clockin.serializers import IntervalWorkSerializer
from datetime import datetime
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from .forms import ClockinForm
from .tables import IntervalTable
from django.utils import timezone
import pytz
import logging

log = logging.getLogger("workTracker")
        
#clockin view
class IndexView(LoginRequiredMixin, ListView):
    model = IntervalWork
    template_name = 'clockin/index.html'
    context_object_name = 'interval'
    ordering = ['id']
    #clockinForm = ClockinForm()
    #group_required = u'company-user'

    def get_context_data(self, **kwargs): 
        context = super(IndexView, self).get_context_data(**kwargs)
        # add data to the context after the request is made
        context['first_name'] = self.request.user.first_name
        #context['user_id'] = self.request.user.id
        context['clockedIn'] = "Clocked In"
        # get only the intervals by the user and today's date
        myHours = IntervalWork.objects.filter(started__date=timezone.now()).filter(user_id=self.request.user.id).order_by('started')
        if not myHours or myHours.last().finished:
            context['clockedIn'] = "Not Clocked In"
        table = IntervalTable(myHours)
        RequestConfig(self.request, paginate=False).configure(table)
        context['table'] = table
        context['myForm'] = ClockinForm()
        #context['lastInterval'] = myHours.last().id
        return context
    
class WorkUpdate(UpdateAPIView):
    queryset = IntervalWork.objects.all()
    serializer_class = IntervalWorkSerializer
    
    def get_queryset(self):
        return IntervalWork.objects.filter(user_id=self.request.user.id).filter(started__date=timezone.now()).order_by('started')
    
class WorkCreate(CreateAPIView):
    queryset = IntervalWork.objects.all()
    serializer_class = IntervalWorkSerializer
    

    
