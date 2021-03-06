"""Album_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from photo.views import getPhoto
from photo.views import getImage
from photo.views import getRecentPhoto
from photo.views import uploadPhoto
from photo.views import uploadImage
from photo.views import searchPhoto
from photo.views import deletePhoto
from photo.views import updatePhoto
from photo.views import deleteSelectedPhoto
from photo.views import signIn

from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^photos/$', getPhoto, name='getPhoto'),
    url(r'^images/$', getImage, name='getImage'),
    url(r'^recentPhotos/$', getRecentPhoto, name='getRecentPhoto'),
    url(r'^upPhoto/$', uploadPhoto, name='uploadPhoto'),
    url(r'^upImage/$', uploadImage, name='uploadImage'),
    url(r'^search/$', searchPhoto, name='searchPhoto'),
    url(r'^delPhoto/$', deletePhoto, name='deletePhoto'),
    url(r'^updatePhoto/$', updatePhoto, name='updatePhoto'),
    url(r'^signIn/$', signIn, name='signIn'),
    url(r'^delSelectedPhoto/$', deleteSelectedPhoto, name='deleteSelectedPhoto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
