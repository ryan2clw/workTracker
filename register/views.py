from django.shortcuts import render
from django.views.generic.edit import FormView
from register.forms import RegistrationFormUniqueEmail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
import requests, json

# Create your views here.
class RegistrationView(FormView):
    """
    Base class for user registration views.
    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationFormUniqueEmail
    success_url = 'menu'
    template_name = 'register'

    def dispatch(self, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        """
        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post(url, values)
        ''' End reCAPTCHA validation '''

        if response.ok:
            new_user = self.register(form)
            success_url = self.success_url
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')    
            
            
    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def register(self, form):
        user = User.objects.create(username=self.request.POST['username'], password=form.fields['password1'])
        user.save()
        return
        """
        Implement user-registration logic here. Access to both the
        request and the registration form is available here.
        """
        #raise NotImplementedError

'''
class ActivationView(TemplateView):
    """
    Base class for user activation views.
    """
    success_url = None
    template_name = 'register.html'

    def get(self, *args, **kwargs):
        """
        The base activation logic; subclasses should leave this method
        alone and implement activate(), which is called from this
        method.
        """
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            signals.user_activated.send(
                sender=self.__class__,
                user=activated_user,
                request=self.request
            )
            success_url = self.get_success_url(activated_user) if \
                (hasattr(self, 'get_success_url') and
                 callable(self.get_success_url)) else \
                self.success_url
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(*args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Implement account-activation logic here.
        """
        raise NotImplementedError
        
'''
