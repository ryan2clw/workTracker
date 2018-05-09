from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from invoice.models import Project
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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

class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'user_id': self.request.user.id})