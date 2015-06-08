from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import ScoreTable, TempTable, MessageTable, \
    Course_info, Class_info, class_table, \
    Student_user, Faculty_user
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


def b_student_query(request, student_id):
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
            if tmp_gpa > 5:
                tmp_gpa = 5
        tmp_node = {'courseID': tmp_class.course_id.course_id,
                    'courseName': tmp_class.course_id.name,
                    'credit': tmp_class.course_id.credits,
                    'score': tmp_score,
                    'gradePoint': tmp_gpa
        }
        scores.append(tmp_node)
    print(scores)
    return HttpResponse(json.dumps(scores), content_type="application/json")


def class_info_query(c_id):
    """
    :param c_id: Class id
    :return: List of student info, in form of {'studentID': '0000000001', 'studentName': 'john'}
    """
    tmp_cla = class_table.objects.filter(class_id=c_id)
    namelist = []
    for stu in tmp_cla:
        tmp_node = {
            'studentID': stu.student_id.id,
            'studentName': stu.student_id.name
        }
        namelist.append(tmp_node)
    return namelist

def b_temp_table_query(request, c_id):
    """

    :param c_id: class_id
    :return: score in temptable
    """
    ret_list = []
    sco_list = TempTable.objects.filter(class_id=c_id)
    for stu in sco_list:
        tmp_score = stu.score
        if tmp_score < 60:
            tmp_gpa = 0
        else:
            tmp_gpa = (tmp_score - 60) / 10 + 1.5
            if tmp_gpa > 5:
                tmp_gpa = 5
        tmp_node = {
            'studentID': stu.student_id.id,
            'studentName': stu.student_id.name,
            'score': tmp_score,
            "gradePoint": tmp_gpa
        }
        ret_list.append(tmp_node)
    print(ret_list)
    return HttpResponse(json.dumps(ret_list), content_type="application/json")


def temp_table_update(c_id, score_list):
    """
    To update the temptable
    :param c_id: class id
    :param score_list: in form of {'studentID': '0000000001', 'score': 100}
    :return:
    """

    for pair in score_list:
        print(pair['score'])
        try:
            tmp_rec = TempTable.objects.get(class_id=c_id, student_id=pair['studentID'])
            tmp_rec.score = pair['score']
            tmp_rec.save()
        except:
            s_id_instance = Student_user.objects.get(id=pair['studentID'])
            c_id_instance = Class_info.objects.get(class_id=c_id)
            TempTable.objects.create(student_id=s_id_instance,
                                     class_id=c_id_instance,
                                     score=pair['score'])

def B_teacher_query(request, teacher_id):
    return HttpResponse(json.dumps(faculty_class_query(teacher_id)), content_type="application/json")

def faculty_class_query(f_id):
    """
    authentication check in need
    :param f_id: faculty_id
    :return: list in form of {}
    """
    info_list = []
    tmp_f = Faculty_user.objects.get(id=f_id)
    cla_list = Class_info.objects.filter(teacher=tmp_f.name)
    for cla in cla_list:
        tmp_node = {
            'classID': cla.class_id,
            'classTime': cla.time,
            'courseID': cla.course_id.course_id,
            'courseName': cla.course_id.name,
            'credits': cla.course_id.credits
        }
        info_list.append(tmp_node)
    return info_list


def b_score_query(c_id):
    """
    Session and authentication check in need
    Responde to front-end score qurey
    :param c_id: class id
    :return: json file
    """
    ret_list = []
    sco_list = ScoreTable.objects.filter(class_id=c_id)
    # print(sco_list)
    for stu in sco_list:
        tmp_score = stu.score
        if tmp_score < 60:
            tmp_gpa = 0
        else:
            tmp_gpa = (tmp_score - 60) / 10 + 1.5
            if tmp_gpa > 5:
                tmp_gpa = 5
        tmp_node = {
            'studentID': stu.student_id.id,
            'studentName': stu.student_id.name,
            'score': tmp_score,
            "gradePoint": tmp_gpa
        }
        ret_list.append(tmp_node)
    print(ret_list)
    return HttpResponse(json.dumps(ret_list), content_type="application/json")


def b_score_modification(c_id, s_id, score, reason):
    """

    :param c_id: class_id
    :param s_id: student_id
    :param score: new score
    :param reason:
    :return:
    """
    # authentication check

    cla = Class_info.objects.get(class_id=c_id)
    from_fac = Faculty_user.objects.filter(name=cla.teacher)
    # cou = Course_info.objects.get(course_id=cla.course_id)
    # cou.class_info_set.all()
    class_set = cla.course_id.class_info_set.all()
    fac_list = []
    for c in class_set:
        fac = Faculty_user.objects.filter(name=c.teacher)
        fac_list.append(fac.id)
        # update_Meaage = MessageTable.objects.create(from_faculty_id=from_fac, to_faculty_id=fac.id,
        #                                 student_id=s_id, class_id=c_id, reason=reason,
        #                                 status=False, score=score)
    print(fac_list)
