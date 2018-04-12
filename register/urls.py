from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import path
from register.views import RegistrationView


urlpatterns = [
    #path('', RegistrationView.as_view(), name='register') 
    #]
    path('', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    ), name='register'),
    #url('^accounts/', include('django.contrib.auth.urls')),
]
'''
urlpatterns = patterns('',
    url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url('^accounts/', include('django.contrib.auth.urls')),

    # rest of your URLs as normal
)
'''
