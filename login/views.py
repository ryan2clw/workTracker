from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from invoice.models import Project
import logging

log = logging.getLogger("workTracker")
        
class CustomLoginview(LoginView):
    def get_redirect_url(self):
        try:
            myProject = Project.objects.get(user_id=self.request.user.id)
            if self.request.user.groups.filter(name="customer").exists():
                return reverse('bill') + "?project=" + myProject.name
        except:
            if self.request.user.groups.filter(name="developer").exists():
                return reverse('clockin')
            return reverse('menu') + "?project=none"
