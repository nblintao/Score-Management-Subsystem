# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django import forms
from .models import ScoreTable, TempTable, MessageTable, \
    Course_info, Class_info, class_table, \
    Student_user, Faculty_user
import json
# User Authentication
from .forms import NameForm
from django.template.context import RequestContext
from django.template import Context
from django.template import Template
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
###
# from dbtest.xls_utils import get_demo_xlsx

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


# Create your views here.
def score_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Uname = request.POST['name'];
            user = authenticate(username=Uname, password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    # should be changed into /SM/index
                    login(request, user)
                    # return redirect(reverse('dbtest.views.score_query',kargs=(Uname),))
                    return HttpResponseRedirect('/SM/query')
                else:
                    return HttpResponseRedirect('/SM/login')
            else:
                return HttpResponseRedirect('/SM/login')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'score_login.html', {'form': form})


@login_required(login_url='/SM/login/')
def score_logout(request):
    logout(request);
    return HttpResponseRedirect('/SM/login')


@login_required(login_url='/SM/login/')
def score_query(request):
    # t = loader.get_template('score_query.html')
    username = request.user.username
    groups = request.user.groups.values_list('name', flat=True);
    if len(groups) > 0:
        Type = groups[0]
    else:
        Type = 'admin'
    # print Type
    if Type == 'student':
        return render(request, 'score_query_student.html')
    elif Type == 'teacher':
        return render(request, 'score_query_faculty.html')
        # return HttpResponse(t.render(id=name))


# you can use login_required to control access
@login_required(login_url='/SM/login/')
@group_required('teacher')
def score_commit(request):
    # t = loader.get_template('score_commit.html')
    # return HttpResponse(t.render(request=request, context = {"UserForm",UserForm}))
    return render(request, 'score_commit.html')


@login_required(login_url='/SM/login/')
@group_required('teacher')
def score_modification(request):
    t = loader.get_template('score_modification.html')
    return HttpResponse(t.render())


def b_student_query(request):
    """
    Query the score records that have already been committed
    :param request: the request object from the browser
    :return: return the json in form of {courseID, courseName,
                                        credit, score, gradePoint}
    """
    # print(request.session)
    # print(student_id)
    student_id = request.user.username
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
    Get the information of the class according to the given class_id
    :param c_id: Class id
    :return: list of student info, in form of {studentID, studentName}
    """
    tmp_cla = class_table.objects.filter(class_id=c_id)
    namelist = []
    for stu in tmp_cla:
        s = TempTable.objects.filter(student_id=stu.student_id.id,
                                     class_id=c_id).first()
        if s is None:
            score = None
        else:
            score = s.score
        tmp_node = {
            'studentID': stu.student_id.id,
            'studentName': stu.student_id.name,
            'score': score
        }
        namelist.append(tmp_node)
    return namelist


def db_temp_table_query(c_id):
    """
    Get the records from the database according to the given class_id
    :param c_id: class_id
    :return: score in temptable in form of {studentID, studentName, score, gradePoint}
    """
    ret_list = []
    sco_list = TempTable.objects.filter(class_id=c_id)
    for stu in sco_list:
        tmp_score = stu.score  # calculate gpa
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
    # return HttpResponse(json.dumps(ret_list), content_type="application/json")
    return ret_list


def b_temp_table_query(request, c_id):
    """
    Respond to the browser request with the score record required
    :param request: the request object from the browser
    :param c_id: class_id from browser
    :return: json file
    """
    return HttpResponse(json.dumps(db_temp_table_query(c_id)), content_type="application/json")


def temp_table_update(c_id, score_list):
    """
    To update the temptable
    :param c_id: class id
    :param score_list: in form of {'studentID': '0000000001', 'score': 100}
    :return:
    """
    print("DEBUG BEGIN")
    print(c_id)
    print(score_list)
    print("DEBUG END")
    for pair in score_list:
        print(pair['score'])
        try:  # upload after init upload, modify the record
            tmp_rec = TempTable.objects.get(class_id=c_id, student_id=pair['studentID'])
            tmp_rec.score = pair['score']
            tmp_rec.save()
        except:  # The first time to upload the records, create tuples
            print(c_id)
            print(type(c_id))
            s_id_instance = Student_user.objects.filter(id=pair['studentID']).first()
            c_id_instance = Class_info.objects.filter(class_id=c_id).first()
            if s_id_instance is None:
                return "上传失败。没有编号为"+pair['studentID']+"的学生。";
            elif c_id_instance is None:
                return "上传失败。没有编号为"+c_id+"的课。";
            else:
                TempTable.objects.create(student_id=s_id_instance,
                                         class_id=c_id_instance,
                                         score=pair['score'])
            # else:
            #     print("s_id_instance None or c_id_instance None")
            #     print(s_id_instance)
            #     print(c_id_instance)
                # return HttpResponse(u'非法班级号或学号')
    return 0

def b_teacher_query(request):
    """
    Respond to the browser request with committed score records
    :param request: the request object from the browser
    :return: json file
    """
    print(request.user.username)
    return HttpResponse(json.dumps(faculty_class_query(request.user.username, False)), content_type="application/json")


def b_teacher_temp_query(request):
    """
    Respond to the browser request with uncommitted score records
    :param request: the request object from the browser
    :return: json file
    """
    return HttpResponse(json.dumps(faculty_class_query(request.user.username, True)), content_type="application/json")


def faculty_class_query(f_id, is_temp):
    """
    authentication check in need
    :param f_id: faculty_id
    :return: list in form of {classID, classTime, courseID, courseName, credits}
    """
    info_list = []
    tmp_f = Faculty_user.objects.get(id=f_id)
    cla_list = Class_info.objects.filter(teacher=tmp_f.name)  # all class list
    tmp_cla_list = []
    for cla in cla_list:
        l = ScoreTable.objects.filter(class_id=cla.class_id).first()
        if is_temp and l is None:  # query uncommitted classes
            tmp_cla_list.append(cla)
        elif not is_temp and l is not None:  # query committed classes
            tmp_cla_list.append(cla)
    cla_list = tmp_cla_list
    for cla in cla_list:
        tmp_node = {  # generate node for list
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
        if tmp_score < 60:  # calculate gpa
            tmp_gpa = 0
        else:
            tmp_gpa = (tmp_score - 60) / 10 + 1.5
            if tmp_gpa > 5:
                tmp_gpa = 5
        tmp_node = {  # generate node for list
                      'studentID': stu.student_id.id,
                      'studentName': stu.student_id.name,
                      'score': tmp_score,
                      "gradePoint": tmp_gpa
        }
        ret_list.append(tmp_node)
    print(ret_list)
    return HttpResponse(json.dumps(ret_list), content_type="application/json")


class ModifyForm(forms.Form):
    classID = forms.DateField()
    studentID = forms.DateField()
    newScore = forms.DateField()
    modifyReason = forms.DateField()



def B_score_modification(request, c_id, s_id):
    print("B_score_modification")
    score = request.POST['newScore']
    reason = request.POST['modifyReason']
    print([c_id, s_id, score, reason])
    # print(request.POST)
    # mf = ModifyForm(request.POST)
    # print(mf.is_valid())
    # print(mf)
    b_score_modification(c_id, s_id, score, reason)
    return HttpResponse("上传成功")


def b_score_modification(c_id, s_id, score, reason):
    """

    :param c_id: class_id
    :param s_id: student_id
    :param score: new score
    :param reason:
    :return:
    """
    cla = Class_info.objects.get(class_id=c_id)  # get class_info object
    stu = Student_user.objects.get(id=s_id)  # get student_user object
    from_fac = Faculty_user.objects.filter(name=cla.teacher).first()
    s = ScoreTable.objects.filter(class_id=c_id, student_id=s_id).first()
    print(s.score)
    print(s.class_id)
    print(s.student_id)
    old_score = s.score
    chief_faculty = cla.course_id.chief_faculty  # generate a new message
    update_message = MessageTable.objects.create(from_faculty_id=from_fac,
                                                 to_faculty_id=chief_faculty,
                                                 student_id=stu, class_id=cla,
                                                 old_score=old_score, new_score=score,
                                                 reason=reason, status=0)
    print(update_message)


def db_query_modify_info(faculty_id):
    """
    Query the MessageTable of records for and from the faculty
    :param faculty_id: as the title
    :return: list in form of {messageID, className, studentID, studentName, old_score,
                                new_score, reason, status}
    """
    modify_list = MessageTable.objects.filter(from_faculty_id=faculty_id)
    audit_list = MessageTable.objects.filter(to_faculty_id=faculty_id)
    ret = []
    modify_node = []
    audit_node = []
    for rec in modify_list:
        if rec.status == 0:  # prevent malicious hacking in js level
            tmp_status = 'pending'
        elif rec.status == 1:
            tmp_status = 'reject'
        else:
            tmp_status = 'admit'
        temp_node = {  # generate node
                       'messageID': rec.id,
                       'className': rec.class_id.course_id.name,
                       'studentID': rec.student_id.id,
                       'studentName': rec.student_id.name,
                       'old_score': rec.old_score,
                       'new_score': rec.new_score,
                       'reason': rec.reason,
                       'status': tmp_status
        }
        modify_node.append(temp_node)
    # print(modify_node)
    ret.append(modify_node)
    for rec in audit_list:
        if rec.status == 0:
            tmp_status = 'pending'
        elif rec.status == 1:
            tmp_status = 'reject'
        else:
            tmp_status = 'admit'
        temp_node = {
            'messageID': rec.id,
            'className': rec.class_id.course_id.name,
            'studentID': rec.student_id.id,
            'studentName': rec.student_id.name,
            'old_score': rec.old_score,
            'new_score': rec.new_score,
            'reason': rec.reason,
            'status': tmp_status
        }
        audit_node.append(temp_node)
    ret.append(audit_node)
    print(ret)
    return ret


def b_query_modify_info(request):
    """
    To query the record of faculty's modification requests
    :param request:
    :return: list of both requests from and in the charge of the faculty
    """
    faculty_id = request.user.username
    return HttpResponse(json.dumps(db_query_modify_info(faculty_id)),
                        content_type="application/json")


def b_sanction_result(requst, msg_id, status):
    """
    To update the message status, usually making it True
    :param msg_id: messageID in the MessageTable
    :param status: how the status changes
    :return: if_succeeded as an HttpResponse object
    """
    try:
        print(status)
        l = MessageTable.objects.get(id=msg_id)
        if status == '1':
            l.status = 2
            l.save()  # update status as 'admitted'
            rec = ScoreTable.objects.filter(class_id=l.class_id.class_id,
                                            student_id=l.student_id.id).first()
            rec.score = l.new_score
            rec.save()  # change score
            return HttpResponse(u'审核成功，成绩将被修改')
        elif status == '0':
            l.status = 1
            l.save()  # update status as 'rejected'
            return HttpResponse(u'审核成功，成绩不同意被修改')
    except:
        return HttpResponse(u'非法记录号')


def b_final_commit(request, c_id):
    """
    Operations on `final commit` from a faculty, in class level
    :param c_id: class_id
    :return:
    """
    fac = Faculty_user.objects.filter(id=request.user.username).first()
    cla = Class_info.objects.filter(class_id=c_id).first()
    if cla.teacher != fac.name:
        return HttpResponse(u'未授权请求!')
    else:
        is_exist = TempTable.objects.filter(class_id=cla.class_id).first()
        if is_exist is None:
            return HttpResponse(u'成绩未上传！')
        score_list = TempTable.objects.filter(class_id=cla.class_id)
        for rec in score_list:  # move score records to ScoreTable
            ScoreTable.objects.create(class_id=rec.class_id,
                                      student_id=rec.student_id,
                                      score=rec.score)
        TempTable.objects.filter(class_id=cla.class_id).delete()
        return HttpResponse(u'提交成功！')


from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from dbtest.models import User
from dbtest.xls_utils import update_score, get_demo_xlsx
# Create your views here.


class XlsxForm(forms.Form):
    xlsx_file = forms.FileField()


import os


def upload_xlsx(request, c_id):
    upload_dir = './upload/'

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

        uf = XlsxForm(request.POST, request.FILES)
        if uf.is_valid():
            xlsx_file = uf.cleaned_data['xlsx_file']

            orig_filename = request.FILES['xlsx_file'].name
            # print(orig_filename)

            user = User()
            user.xlsx_file = xlsx_file
            user.save("{}.xlsx".format(orig_filename))

            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)

            hr = update_score(upload_dir + '{}'.format(orig_filename), c_id)
            try:
                os.remove(upload_dir + '{}'.format(orig_filename))
            except:
                print("Cannot remove file" + upload_dir + '{}'.format(orig_filename))
            if hr:
                return HttpResponse(hr)
            # else:
            #     return HttpResponse('upload ok!')
            return HttpResponse('upload ok!')
    else:
        uf = XlsxForm()
    return render_to_response('score_commit.html', {'uf': uf})
    # return render(request, 'score_commit.html')


def download_xlsx(request, c_id):
    download_dir = './download/'

    # if request.method is 'GET':
    # print(request.GET)

    get_demo_xlsx(c_id)

    with open(download_dir + '/demo.xlsx', 'rb') as file:
        c = file.read()

    response = HttpResponse(c)
    response['Content-Type'] = 'application/octet_stream'
    response['Content-Disposition'] = 'attachment; filename="sample.xlsx"'

    return response 
