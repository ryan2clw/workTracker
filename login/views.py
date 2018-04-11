from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from invoice.models import Project
import logging

log = logging.getLogger("workTracker")
        
class CustomLoginview(LoginView):
    
    def get_redirect_url(self):
        if self.request.user.groups.filter(name="customer").exists():
            myProject = Project.objects.get(user_id=self.request.user.id)
            return reverse('bill') + "?project=" + myProject.name
            #return 'invoice'
        return super().get_redirect_url()

