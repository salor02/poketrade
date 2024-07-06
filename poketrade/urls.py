"""
URL configuration for poketrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .initcmds import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^home\/$|^$', homeView, name = 'home'),
    path('collection/', include('collection.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('api/v1/', include('api.urls')),
    path('user/', include('user.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#erase_db()
init_collection_db()
#erase_user_DB()
#init_user_DB()
#erase_marketplace_db()
#init_marketplace_db()
