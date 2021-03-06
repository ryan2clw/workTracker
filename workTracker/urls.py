from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from login.views import CustomLoginview, CustomObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('menu.urls')),
    path('login/', CustomLoginview.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clockin/', include('clockin.urls')),
    path('invoice/', include('invoice.urls')),
    path('menu/', include('menu.urls')),
    path('developer/', include('developer.urls')),
    path('project/', include('project.urls')),
    path('register/', include('register.urls')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', CustomObtainAuthToken.as_view()),
]













































"""workTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
