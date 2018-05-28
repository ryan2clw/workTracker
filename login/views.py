from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from invoice.models import Project
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import logging

log = logging.getLogger("workTracker")
        
class CustomLoginview(LoginView):
    
    # if they are a customer with project, go there, developer with a project, go there, else, make-project page
    def get_redirect_url(self):
        if(self.request.user.is_anonymous):
            return reverse('login') # MARK TO DO: ADD EPIC FAILURE WARNING TO LOGIN
        myProjects = Project.objects.filter(members=self.request.user)
        if self.request.user.groups.filter(name="customer").exists() and len(myProjects) > 0:
            return reverse('bill') + "?project=" + myProjects.last().name 
        if self.request.user.groups.filter(name="developer").exists() and len(myProjects) > 0:
            return reverse('clockin')
        return reverse('project')

class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'user_id': self.request.user.id,
                         'first_name': user.first_name})