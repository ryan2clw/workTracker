from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from register.forms import RegistrationForm
from django.urls import path
from django.conf.urls import url
from register.views import signup, activate

urlpatterns = [
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    activate, name='activate'),
    #path('activate',activate, name='activate'),
    path('activate/<slug:uid>/<slug:token>/', activate, name='activate'),
    path('', signup, name='register')
]










'''
    #path('', RegistrationView.as_view(), name='register') 
    #]
    path('', RegistrationView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    ), name='register'),
    #url('^accounts/', include('django.contrib.auth.urls')),
]

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
