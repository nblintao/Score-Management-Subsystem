from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
import json

# Create your views here.

def score_query(request):
    t = loader.get_template('score_query.html')
    return HttpResponse(t.render())
    # return HttpResponse("Here should be a form with a query button")

def B_student_query(request, student_id):
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
    }    
    ]
    
    return HttpResponse(json.dumps(scores), content_type="application/json")