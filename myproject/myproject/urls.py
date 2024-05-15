"""
URL configuration for myproject project.

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
from smartbin import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from smartbin.views import logout_view
from django.urls import path
from smartbin.firebase_listner import listen_for_bin_level_changes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('binview/', views.bin_view, name='binview'),
    path('login/', auth_views.LoginView.as_view(template_name='smartbin/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-bin/', views.create_bin, name='create_bin'),
]

listen_for_bin_level_changes()