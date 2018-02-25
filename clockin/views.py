from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
from clockin.models import IntervalWork
from datetime import datetime
import logging

log = logging.getLogger("workTracker")
        
#clockin view
class IndexView(LoginRequiredMixin, TemplateView):
    log.debug("Entering clockin view")
    template_name = 'clockin/index.html'
    intervalWork = IntervalWork()
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        '''
        if datetime.now().weekday() < 5 and 8 < datetime.now().hour < 18:
            context['open'] = True
        else:
            context['open'] = False
        '''
        return context
