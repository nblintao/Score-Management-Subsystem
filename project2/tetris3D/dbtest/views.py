from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
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
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group, Permission
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
###

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
            Uname=request.POST['name'];
            user = authenticate(username=Uname, password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    # should be changed into /SM/index
                    login(request, user)
                    #return redirect(reverse('dbtest.views.score_query',kargs=(Uname),))
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
    t = loader.get_template('score_query.html')
    username = request.user.username
    groups=request.user.groups.values_list('name',flat=True);
    if len(groups)>0:
        Type=groups[0]
    else:
        Type='admin'
    #print Type
    return render(request, 'score_query.html', {'id': username, 'type': Type})
    #return HttpResponse(t.render(id=name))


# you can use login_required to control access
@login_required(login_url='/SM/login/')
@group_required('teacher')
def score_commit(request):
    t = loader.get_template('score_commit.html')
    return HttpResponse(t.render())


@login_required(login_url='/SM/login/')
@group_required('teacher')
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


def b_teacher_query(request, teacher_id):
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
    cla = Class_info.objects.get(class_id=c_id)
    from_fac = Faculty_user.objects.filter(name=cla.teacher)
    s = ScoreTable.objects.filter(class_id=c_id, student_id=s_id)
    old_score = s.score
    chief_faculty = cla.course_id.chief_faculty
    update_message = MessageTable.objects.create(from_faculty_id=from_fac.id,
                                                 to_faculty_id=chief_faculty.id,
                                                 student_id=s_id, class_id=c_id,
                                                 old_score=old_score, new_score=score,
                                                 reason=reason, status=False)
    print(update_message)


def b_query_modify_info(faculty_id):
    """
    To query the record of faculty's modification requests
    :param faculty_id:
    :return: list of both requests from and in the charge of the faculty
    """
    modify_list = MessageTable.objects.filter(from_faculty_id=faculty_id)
    audit_list = MessageTable.objects.filter(to_faculty_id=faculty_id)
    ret = []
    modify_node = []
    audit_node = []
    for rec in modify_list:
        temp_node = {
            'messageID': rec.id,
            'className': rec.class_id.course_id.name,
            'studentID': rec.student_id.student_id,
            'studentName': rec.student_id.name,
            'old_score': rec.old_score,
            'new_score': rec.new_score,
            'reason': rec.reason,
            'status': rec.status
        }
        modify_node.append(temp_node)
    print(modify_node)
    ret.append(modify_node)
    for rec in audit_list:
        temp_node = {
            'messageID': rec.id,
            'className': rec.class_id.course_id.name,
            'studentID': rec.student_id.student_id,
            'studentName': rec.student_id.name,
            'old_score': rec.old_score,
            'new_score': rec.new_score,
            'reason': rec.reason,
            'status': rec.status
        }
        audit_node.append(temp_node)
    ret.append(audit_node)
    print(ret)
    return HttpResponse(json.dumps(ret), content_type="application/json")


def b_sanction_result(msg_id, status):
    """
    To update the message status, usually making it True
    :param msg_id: messageID in the MessageTable
    :param status: how the status changes
    :return:
    """
    try:
        l = MessageTable.objects.get(id=msg_id)
        l.status = status
        rec = ScoreTable.objects.filter(class_id=l.class_id.class_id,
                                        student_id=l.student_id.student_id).first()
        rec.score = l.new_score
        return HttpResponse('Audit Done, Score modified.')
    except:
        return HttpResponse('invalid record id.')


from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from dbtest.models import User
from dbtest.xls_utils import update_score
# Create your views here.


class UserForm(forms.Form):
    xlsx_file = forms.FileField()


import os


def upload_xlsx(request):
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            xlsx_file = uf.cleaned_data['xlsx_file']

            user = User()
            user.xlsx_file = xlsx_file
            user.save()
            update_score('./upload/sample.xlsx')
            os.remove('./upload/sample.xlsx')
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render_to_response('score_upload.html', {'uf': uf})


def download_xlsx(request):
    with open('./download/sample.xlsx') as file:
        c = file.read()

    return HttpResponse(c)
