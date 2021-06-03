"""road_situation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from road import views

urlpatterns = [
    url(r'^$', views.home, name='Home'),

    url(r'^events', views.get_events, name='Get all events'),

    url(r'^upload', views.post_image, name='Post image'),

    url(r'^image', views.get_image, name='Get image'),

    url(r'^delete', views.delete_item, name='Delete item in the database')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
