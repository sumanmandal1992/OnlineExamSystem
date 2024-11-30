from django.db.models.deletion import models
from django.db.models.fields.json import json
from django.shortcuts import HttpResponseRedirect, render
from django.contrib import admin
from django.core.management import call_command
import hashlib as hash
import ast, sys

from django.views.decorators.csrf import csrf_exempt

from .models import *

from .forms import AdminForm, StudentLoginForm, QnsDbFileForm, QuestionForm, StdDbFileForm


# Create your views here.
# Convert to class object
def get_class(class_name):
    return getattr(sys.modules[__name__], class_name)

# Global data
class SharedData:
    ansdb = ans_1234.objects
    qnsdb = Questions.objects
    qns_serial = 0
    qns_max = qnsdb.values().count()
    anslist = ansdb.values_list('qn_no', flat=True)

# Home page
def index_page(request):
    template = 'index.html'
    context = { 'stdlogin': StudentLoginForm(), 'adminform': AdminForm() }
    return render(request, template, context)


# Students login form
def get_std_login_info(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            stdid = form.cleaned_data['student_id']
            stdpwd = form.cleaned_data['std_passwd'].encode('ascii')
            # Answer database
            ansdbclass = get_class('ans_'+stdid)
            SharedData.ansdb = ansdbclass.objects

            # Encryption
            sha = hash.sha512()
            sha.update(stdpwd)
            stdpwd = sha.hexdigest()

            stdacdb = StudentAccounts.objects.filter(roll=stdid).values()
            stddbpwd = None
            if stdacdb.exists():
                stddbpwd = stdacdb[0]['passwd']

            if stddbpwd == stdpwd:
                return HttpResponseRedirect("/exam/qns/")
            else:
                form = StudentLoginForm(log_failed=1)
                template = 'index.html'
                context = { 'stdlogin': form, 'adminform': AdminForm() }
                return render(request, template, context)
    else:
        form = StudentLoginForm()
        template = 'index.html'
        context = { 'stdlogin': form }
        return render(request, template, context)


def exam_qns_and_save_next(request):
    anslist = SharedData.ansdb.values_list('qn_no', flat=True)
    anslist = json.dumps(list(SharedData.anslist))
    if request.method == "POST":
        form = QuestionForm(request.POST)
        val = request.POST.get('choice')

        if val != None:
            choice=ast.literal_eval(val)
            form.fields['choice'].choices=[(choice, choice)]

        if form.is_valid():
            choice_select = None
            if form.cleaned_data['choice']:
                choice_select = int(form.cleaned_data['choice'])

            if SharedData.qnsdb.exists() and choice_select != None:
                SharedData.ansdb.update_or_create(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no'], defaults={'choice': choice_select})

            if SharedData.qns_serial<(SharedData.qns_max-1):
                SharedData.qns_serial += 1
            else:
                SharedData.qns_serial = 0
            chs = None
            qn_no = None
            question = None
            if SharedData.qnsdb.exists():
                chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
                qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
                question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']

            ans = None
            if SharedData.ansdb.exists():
                if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                    ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']
            form = QuestionForm(chs=chs, ans=ans)
            context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form, 'anslist': anslist }
            template = 'exam.html'
            return render(request, template, context)
    else:
        chs = None
        qn_no = None
        question = None
        if SharedData.qnsdb.exists:
            chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
            qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
            question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']
        ans = None
        if SharedData.ansdb.exists():
            if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']
        form = QuestionForm(chs=chs, ans=ans)
        context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form, 'anslist': anslist }
        template = 'exam.html'
        return render(request, template, context)


def qns_save_preview(request):
    global i
    anslist = SharedData.ansdb.values_list('qn_no', flat=True)
    anslist = json.dumps(list(anslist))
    if request.method == "POST":
        val=request.POST.get('choice')
        form = QuestionForm(request.POST)
        if val != None:
            choice=ast.literal_eval(val)
            form.fields['choice'].choices=[(choice, choice)]

        if form.is_valid():
            choice_select = None
            if form.cleaned_data['choice']:
                choice_select = int(form.cleaned_data['choice'])

            if SharedData.qnsdb.exists() and choice_select != None:
                SharedData.ansdb.update_or_create(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no'], defaults={'choice': choice_select})

            if SharedData.qns_serial>0:
                SharedData.qns_serial -= 1
            else:
                SharedData.qns_serial = SharedData.qns_max-1
            chs = None
            qn_no = None
            question = None
            if SharedData.qnsdb.exists():
                chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
                qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
                question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']

            ans = None
            if SharedData.ansdb.exists():
                if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                    ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']
            form = QuestionForm(chs=chs, ans=ans)
            context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form, 'anslist': anslist }
            template = 'exam.html'
            return render(request, template, context)
    else:
        chs = None
        qn_no = None
        question = None
        if SharedData.qnsdb.exists():
            chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
            qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
            question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']
        ans = None
        if SharedData.ansdb.exists():
            if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']
        form = QuestionForm(chs=chs, ans=ans)
        context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form, 'anslist': anslist }
        template = 'exam.html'
        return render(request, template, context)


def qns_save_jump(request):
    anslist = SharedData.ansdb.values_list('qn_no', flat=True)
    anslist = json.dumps(list(anslist))
    if request.method == "POST":
        val=request.POST.get('choice')
        form = QuestionForm(request.POST)
        if val != None:
            choice=ast.literal_eval(val)
            form.fields['choice'].choices=[(choice, choice)]

        if form.is_valid():
            choice_select = None
            if form.cleaned_data['choice']:
                choice_select = int(form.cleaned_data['choice'])

            if SharedData.qnsdb.exists() and choice_select != None:
                SharedData.ansdb.update_or_create(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no'], defaults={'choice': choice_select})

            SharedData.qns_serial = int(request.POST.get('qn_jump'))-1

            chs = None
            qn_no = None
            question = None
            if SharedData.qnsdb.exists():
                chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
                qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
                question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']

            ans = None
            if SharedData.ansdb.exists():
                if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                    ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']

            form = QuestionForm(chs=chs, ans=ans)
            context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form, 'anslist': anslist }
            template = 'exam.html'
            return render(request, template, context)
    else:
        chs = None
        qn_no = None
        question = None
        if SharedData.qnsdb.exists():
            chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
            qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
            question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']

        ans = None
        if SharedData.ansdb.exists():
            if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']

        form = QuestionForm(chs=chs, ans=ans)
        context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form, 'anslist': anslist }
        template = 'exam.html'
        return render(request, template, context)


def submit_exam(request):
    if request.method == "POST":
        val=request.POST.get('choice')
        form = QuestionForm(request.POST)
        if val != None:
            choice=ast.literal_eval(val)
            form.fields['choice'].choices=[(choice, choice)]

        if form.is_valid():
            choice_select = None
            if form.cleaned_data['choice']:
                choice_select = int(form.cleaned_data['choice'])

            if SharedData.qnsdb.exists() and choice_select != None:
                SharedData.ansdb.update_or_create(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no'], defaults={'choice': choice_select})

            template = 'success.html'
            return render(request, template)
    else:
        chs = None
        qn_no = None
        question = None
        if SharedData.qnsdb.exists():
            chs = ast.literal_eval(SharedData.qnsdb.values()[SharedData.qns_serial]['choices'])
            qn_no = SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']
            question = SharedData.qnsdb.values()[SharedData.qns_serial]['questions']

        ans = None
        if SharedData.ansdb.exists():
            if SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).exists():
                ans = SharedData.ansdb.filter(qn_no=SharedData.qnsdb.values()[SharedData.qns_serial]['qn_no']).values()[0]['choice']

        form = QuestionForm(chs=chs, ans=ans)
        context = { 'qn_max': SharedData.qns_max, 'qn_no': qn_no, 'question': question, 'qform': form }
        template = 'exam.html'
        return render(request, template, context)


def secure_exam_form(request):
    template = 'exam.html'
    return render(request, template)


# Admin login form
def get_admin_info(request):
    if request.method == "POST":
        form = AdminForm(request.POST)
        if form.is_valid():
            adminid = form.cleaned_data['admin_id']
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['admin_passwd']
            sha = hash.sha512()
            sha.update(passwd.encode('ascii'))
            passwd = sha.hexdigest()

            adminacdb = AdminAccount.objects.filter(user_name=username, user_id=adminid).values()
            dbpasswd = None
            if adminacdb.exists():
                dbpasswd = adminacdb[0]['password']

            if dbpasswd == passwd:
                return HttpResponseRedirect("/super/upload/")
            else:
                form = AdminForm(log_failed=1)
                template = 'index.html'
                context = { 'adminform': form, 'stdlogin': StudentLoginForm() }
                return render(request, template, context)
    else:
        form = AdminForm()
    template = 'index.html'
    context = { 'adminform': form }
    return render(request, template, context)


def admin_panel(request):
    template='super.html'
    context={'stddbform': StdDbFileForm(), 'qnsdbform': QnsDbFileForm()}
    return render(request, template, context)


def upload_std_db_file(request):
    if request.method == "POST":
        form = StdDbFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        handle_uploaded_file(file)
        return HttpResponseRedirect("/super/upload/")
    else:
        form = StdDbFileForm()
    template = 'super.html'
    context = { 'stddbform': form, 'qnsdbform': QnsDbFileForm() }
    return render(request, template, context)


def upload_qns_db_file(request):
    if request.method == "POST":
        form = QnsDbFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        handle_uploaded_file(file)
        return HttpResponseRedirect("/super/upload/")
    else:
        form = QnsDbFileForm()
    template = 'super.html'
    context = { 'qnsdbform': form, 'stddbform': StdDbFileForm() }
    return render(request, template, context)


def handle_uploaded_file(f):
    print("Uploaded file: ", f)
    #with open('some/file/name.txt', 'wb+') as dest:
    #    for chunk in f.chunks():
    #        dest.write(chunk)


def generate_std_account(name):
    name = 'Std'
    attrs = {
            'qn_no': models.IntegerField(max_length=4, unique=True),
            'choice': models.IntegerField(max_length=2),
            '__module__': 'pages.models'
    }
    std = type(name, (models.Model,), attrs)
    admin.site.register(std)
    call_command('makemigrations')
    call_command('migrate')
