"""qishu URL Configuration

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
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView
from xadmin.plugins import xversion
import xadmin

# django处理静态文件内容
from django.views.static import serve
from .settings import MEDIA_ROOT

#version模块自动注册需要版本控制的 Model
xversion.register_models()

xadmin.autodiscover()

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    path('novel/', include('novel.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('search/', include('haystack.urls')),
    path('account/', include('django.contrib.auth.urls')),
    url(r'^captcha/', include('captcha.urls')),
    path('xadmin/', xadmin.site.urls),
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path(r'', RedirectView.as_view(url='/novel/')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns