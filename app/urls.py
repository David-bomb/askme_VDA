from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
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
    path('answer/<int:answer_id>/like_async', views.answer_like_async, name='answer_like_async'),
    path('answer/<int:answer_id>/mark_correct', views.mark_answer_correct, name='mark_correct'),

])

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)