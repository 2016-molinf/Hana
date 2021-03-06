"""Chemdbweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

import Chemdb.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'structures/(\d+)', Chemdb.views.structure_image),
    url(r'home', Chemdb.views.index),
    url('insert', Chemdb.views.insert),
    url('search', Chemdb.views.search),
    url('chemical', Chemdb.views.chemical),
    url('about', Chemdb.views.about),
    url('contact', Chemdb.views.contact),
    url(r'', Chemdb.views.index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)