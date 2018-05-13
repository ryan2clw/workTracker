from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from clockin.models import IntervalWork # TO DO: ADD MODEL AND TEMPLATE

class ProjectView(LoginRequiredMixin, ListView):
    model = IntervalWork
    template_name = 'project/project.html'

    def get_context_data(self, **kwargs): 
        # Initializes the state of the view
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        print(context['first_name'])
        return context
