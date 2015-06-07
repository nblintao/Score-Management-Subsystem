from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
import json
from dbtest.models import ScoreTable, TempTable, MessageTable, Course_info, Class_info

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
    scores = []
    ret = ScoreTable.objects.filter(student_id=student_id)

    for stu in ret:
        tmp_score = stu.score
        tmp_class = stu.class_id
        if tmp_score < 60:
            tmp_gpa = 0
        else:
            tmp_gpa = (tmp_score - 60) / 10 + 1.5
        tmp_node = {'courseID': tmp_class.course_id.course_id,
                    'courseName': tmp_class.course_id.name,
                    'credit': tmp_class.course_id.credits,
                    'score': tmp_score,
                    'gradePoint': tmp_gpa, }
        scores.append(tmp_node)

    '''
    scores = [
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
    }    
    ]
    '''
    print(scores)
    return HttpResponse(json.dumps(scores), content_type="application/json")