from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
#from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django_tables2 import RequestConfig
from clockin.models import IntervalWork
from datetime import datetime
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from .forms import ClockinForm
from .tables import IntervalTable
import pytz
import logging

log = logging.getLogger("workTracker")
        
#clockin view
class IndexView(LoginRequiredMixin, ListView): # removed GroupRequiredMixin, 
    model = IntervalWork
    template_name = 'clockin/index.html'
    context_object_name = 'interval'
    ordering = ['id']
    #group_required = u'company-user'

    def get_context_data(self, **kwargs):
        kwargs['user_id'] = self.request.user.id 
        context = super(IndexView, self).get_context_data(**kwargs)
        #context['user'] = str(self.request.user)
        #table = IntervalTable(IntervalWork.objects.filter(self.request.user).order_by('-pk'))
        table = IntervalTable(IntervalWork.objects.filter(user_id=self.request.user.id).order_by('-pk'))
        RequestConfig(self.request, paginate={'per_page': 5}).configure(table)
        context['table'] = table
        return context
        
class WorkCreate(UpdateView):
    log.debug("Entering WorkCreate view")
    
class WorkUpdate(UpdateView):
    log.debug("Entering WorkUpdate view")
    model = IntervalWork
    form_class = ClockinForm
    
