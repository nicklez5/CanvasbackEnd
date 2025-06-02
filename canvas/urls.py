"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include
from .views import get_csrf_token
from rest_framework import routers 
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/get-csrf-token/", get_csrf_token),
    path('users/', include('users.urls')),
    path('assignments/', include('assignments.urls')),
    path('lectures/', include('lectures.urls')),
    path('courses/', include('course.urls')),
    path('profiles/',include('profiles.urls')),
    path('canvas/', include('mycanvas.urls')),
    path('tests/',include('tests.urls')),
    path('threads/',include('threads.urls')),
    path('messages/',include('message.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)