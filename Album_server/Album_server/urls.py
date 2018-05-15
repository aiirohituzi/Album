"""Album_server URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from photo.views import getPhoto
from photo.views import getImage
from photo.views import uploadPhoto
from photo.views import uploadImage
from photo.views import searchPhoto
from photo.views import deletePhoto
from photo.views import updatePhoto

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^photos/$', getPhoto, name='getPhoto'),
    url(r'^images/$', getImage, name='getImage'),
    url(r'^upPhoto/$', uploadPhoto, name='uploadPhoto'),
    url(r'^upImage/$', uploadImage, name='uploadImage'),
    url(r'^search/$', searchPhoto, name='searchPhoto'),
    url(r'^delPhoto/$', deletePhoto, name='deletePhoto'),
    url(r'^updatePhoto/$', updatePhoto, name='updatePhoto'),
]
