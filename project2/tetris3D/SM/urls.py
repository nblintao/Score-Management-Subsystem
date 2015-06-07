from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^score_query', views.score_query),
    url(r'^B_student_query/(?P<student_id>\d{4})', views.B_student_query),
]
