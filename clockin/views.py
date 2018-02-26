from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
from clockin.models import IntervalWork
from datetime import datetime
import logging

log = logging.getLogger("workTracker")
        
#clockin view
class IndexView(LoginRequiredMixin, ListView):
    log.debug("Entering clockin view")
    template_name = 'clockin/index.html'
    #intervalWork = IntervalWork()
    model = IntervalWork
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        '''
        PASS STUFF TO THE VIEW HERE
        if datetime.now().weekday() < 5 and 8 < datetime.now().hour < 18:
            context['open'] = True
        else:
            context['open'] = False
        '''
        return context
        
class WorkCreate(CreateView):
    model = IntervalWork
    #success_url = reverse_lazy('clockin')
    #fields = ['started', 'finished', 'comments']

class WorkUpdate(UpdateView):
    model = IntervalWork
    #success_url = reverse_lazy('clockin')
    #fields = ['name', 'ip', 'order']
