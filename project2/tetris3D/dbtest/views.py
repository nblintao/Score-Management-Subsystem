from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
import json

# Create your views here.

def score_login(request):
    print(request.method)
    if request.method == 'GET':
        t = loader.get_template('score_login.html')
        return HttpResponse(t.render())
    else:
        print("other")



def score_query(request):
    t = loader.get_template('score_query.html')
    return HttpResponse(t.render())

def score_commit(request):
    t = loader.get_template('score_commit.html')
    return HttpResponse(t.render())

def score_modification(request):
    t = loader.get_template('score_modification.html')
    return HttpResponse(t.render())

def B_student_query(request, student_id):
    print(request.session)
    print(student_id)

    scores=[
    {
    'courseID':'111111',
    'courseName':'哈哈哈',
    'score':87,
    'credit':1,
    'gradePoint':4.2
    },
    {
    'courseID':'111111',
    'courseName':'哈哈哈',
    'score':87,
    'credit':1,
    'gradePoint':4.2
    },
    {
    'courseID':'1111331',
    'courseName':'喂喂喂',
    'score':77,
    'credit':1,
    'gradePoint':3.2
    },
    {
    'courseID':'1111331',
    'courseName':'喂喂喂',
    'score':67,
    'credit':1,
    'gradePoint':2.2
    },      
    ]

    return HttpResponse(json.dumps(scores), content_type="application/json")