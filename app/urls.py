"""
URL configuration for askme_VDA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>', views.question, name='question'),
    path('hot', views.hot, name='hot'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('tag/<str:tag>', views.tag, name='tag'),
    path('settings', views.settings, name='settings'),
    path('404', views.Err404, name='404'),
    path('logout', views.logout, name='logout'),
    path('<int:question_id>/like_async', views.like_async, name='like_async'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)