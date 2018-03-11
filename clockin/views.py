from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import UpdateAPIView, CreateAPIView
from django_tables2 import RequestConfig
from clockin.models import IntervalWork
from clockin.serializers import IntervalWorkSerializer
from django.utils import timezone
from pytz import timezone as pytzTZ
from .forms import ClockinForm
from .tables import IntervalTable
import logging

log = logging.getLogger("workTracker")
        
# Clockin View

class IndexView(LoginRequiredMixin, ListView):
    model = IntervalWork
    template_name = 'clockin/index.html'
    context_object_name = 'interval'
    ordering = ['id']
    
    def value(self):
        return sum([Card.values[card.rank] for card in self.cards])
    
    def totalHours(hoursList): # iterator syntax for speed
        return sum(interval.timeApart() for interval in hoursList)

    def get_context_data(self, **kwargs): 
        # Initializes the state of the view
        context = super(IndexView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['clockedIn'] = "Clocked In"
        myHours = IntervalWork.objects.filter(user_id=self.request.user.id).order_by('started')
        context['myHours'] = myHours
        log.debug(myHours)
        #filter(started__date=timezone.now().astimezone(pytzTZ('US/Eastern')).date())\
        #myHours = [interval for interval in myHours if interval.started.date() == timezone.now().astimezone(pytzTZ('US/Eastern')).date()]
        #log.debug(myHours)
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
    serializer_class = IntervalWorkSerializer
    def get_queryset(self):
        return IntervalWork.objects.filter(user_id=self.request.user.id).order_by('started')#.filter(started__date=timezone.now())
    
class WorkCreate(CreateAPIView):
    queryset = IntervalWork.objects.all()
    serializer_class = IntervalWorkSerializer
    

    
