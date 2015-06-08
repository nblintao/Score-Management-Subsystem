from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login', views.score_login),
    url(r'^query', views.score_query),
    url(r'^commit', views.score_commit),
    url(r'^modification', views.score_modification),
    url(r'^B_student_query/(?P<student_id>\d+)', views.B_student_query),
    url(r'^B_teacher_query/(?P<teacher_id>\d+)', views.B_teacher_query),
    url(r'^B_download/(?P<course_id>\d+)', views.B_download),
]
