"""DaidaiStudy URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from app01 import views
from django.views.static import serve
from django.conf import settings
from app01 import urls as app01urls
from stark.service.stark import site


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'stark/', site.urls),
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^reg/', views.register),
    url(r'^get_valid_img.png/', views.get_valid_img),
    url(r'^upload/', views.upload),
    url(r'^pc-geetest/register', views.get_geetest),
    url(r'check_username_exist/$', views.check_username_exist),
    url(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    url(r'^blog/', include(app01urls)),
]
