"""digigru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apiv1 import urls as apiv1_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name="home"),
    path('bbs/', include('bbs.urls'), name="bbs"),
    path('ringi/', include('ringi.urls'), name="ringi"),
    path('member/',include('member.urls'), name="member"),
    path('tool/',include('tool.urls'), name="tool"),
    path('work/',include('work.urls'), name="work"),
    path('blog/',include('blog.urls'), name="blog"),
    path('account/', include('account.urls'), name="account"),
    path('issue/', include('issue.urls')),

    url(r'mdeditor/', include('mdeditor.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/v1/', include('apiv1.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)