from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Max
import datetime
from django.contrib import messages
from judger import forms
from .models import Problem, Code, User, Contest, Editable
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.utils import timezone


# Create your views here.
def judge_home(request):
    msg_ls = Code.objects.all()[:4]
    editable = get_object_or_404(Editable, pk=1)
    try:
        user = get_object_or_404(User, username=request.session['username'])
    except:
        user = "当前未登陆"
    context = {'msg_ls': msg_ls, 'e': editable, 'user': user}
    return render(request, 'JudgeHome.html', context)


def problem(request, problem_id):
    prob = get_object_or_404(Problem, problem_id=problem_id)
    context = {'problem_id': prob.problem_id,
               'time_limit': prob.time_limit_ms,
               'memory_limit': prob.memory_limit_kb / 1000,
               'title': prob.title, 'description': prob.description,
               'input_format': prob.input_format,
               'output_format': prob.output_format,
               'sample_input': prob.sample_input,
               'sample_output': prob.sample_output,
               'range_and_hint': prob.range_and_hint}
    return render(request, 'Problem.html', context)


def problem_set(request):
    prob_ls = Problem.objects.order_by('problem_id')
    paginator = Paginator(prob_ls, 15)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            probs = paginator.page(page)
        except PageNotAnInteger:
            probs = paginator.page(1)
        except InvalidPage:
            return render(request, 'ProblemSetError.html')
    context = {'problem_list': probs}
    return render(request, 'ProblemSet.html', context)


def submit_code(request, problem_id):
    code = Code.objects.latest('code_id')
    prob = get_object_or_404(Problem, problem_id=problem_id)
    codex = Code(code_id=code.code_id+1, problem=prob)
    # 判断是否为空，若为空就直接返回错误
    if not request.POST['code'].strip():
        return render(request, 'error.html', {'error_type': 'code_empty'})
    codex.code_itself = request.POST['code']
    codex.language = request.POST['language']
    try:
        postman = get_object_or_404(User, username=request.session['username'])
        codex.postman = postman
        codex.WJ = True
        codex.save()
        return render(request, 'Submitted.html')
    except:
        return render(request, 'error.html', {'error_type': 'not_logged_in'})


def register(request):
    if request.method == "POST":
        register_form = forms.UserForm(request.POST)
        message = "填写内容出错，请检查"
        if register_form.is_valid():
            usr = register_form.cleaned_data['usr']
            pwd = register_form.cleaned_data['pwd']
            try:
                user = User(username=usr, password=pwd)
                easiest_problem = get_object_or_404(Problem, problem_id=19960207)
                user.save()
                user.accepted.add(easiest_problem)
                return render(request, 'Registered.html', locals())
            except:
                message = "不能注册重复的用户，请更换用户名"
        return render(request, 'Register.html', locals())
    else:
        register_form = forms.UserForm()
        return render(request, 'Register.html', locals())


def login(request):
    if request.session.get('logged_in', None):
        return redirect("/JudgeHome/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "填写内容出错，请检查"
        if login_form.is_valid():
            usr = login_form.cleaned_data['usr']
            pwd = login_form.cleaned_data['pwd']
            try:
                user = User.objects.get(username=usr)
                if user.password == pwd:
                    request.session['logged_in'] = True
                    request.session['username'] = usr
                    request.session['password'] = pwd
                    user.logged_in = True
                    user.save()
                    return render(request, 'LoginSucceed.html')
                else:
                    message = "密码错误"
            except:
                message = "用户不存在"
        return render(request, 'Login.html', locals())

    else:
        login_form = forms.UserForm()
        return render(request, 'Login.html', locals())


def logout(request):
    if not request.session.get('logged_in', None):
        return redirect('/JudgeHome/')
    user = User.objects.get(username=request.session['username'])
    user.logged_in = False
    user.save()
    request.session.flush()
    return render(request, 'LoggedOut.html')


def status(request):
    code_ls = Code.objects.all()[:20]
    for i in code_ls:
        if i.AC:
            postman = i.postman
            postman.accepted.add(i.problem)
            # 因为有道送命题，所以这里通过数减去1道
            postman.ac_count = postman.accepted.count()-1
            postman.save()
    context = {'code_list': code_ls}
    return render(request, 'Status.html', context)


def contest_list(request):
    cont_ls = Contest.objects.all()
    for i in cont_ls:
        i.set_active()
    cont_ls = Contest.objects.all()
    context = {'contest_list': cont_ls}
    return render(request, 'ContestList.html', context)


def contest(request, contest_id):
    cont = get_object_or_404(Contest, contest_id=contest_id)
    try:
        user = get_object_or_404(User, username=request.session['username'])
        part = False  # 代表是否参与了比赛
        if user in cont.contestant.all():
            part = True
        if not cont.is_active:
            return render(request, 'JudgeHome.html')
        prob_ls = cont.problems
        context = {'contest': cont, 'problem_list': prob_ls, 'part': part}
        return render(request, 'Contest.html', context)
    except:
        context = {'error_type': 'not_logged_in'}
        return render(request, 'error.html', context)


def ranking(request):
    user_ls = User.objects.all()[:15]
    context = {'user_ls': user_ls}
    return render(request, 'Ranking.html', context)


def participate(request, contest_id):
    # 参加比赛
    try:
        cont = get_object_or_404(Contest, contest_id=contest_id)
        user = get_object_or_404(User, username=request.session['username'])
        context = {'contest': cont, 'problem_list': cont.problems, 'part': 'Successfully participated!'}
        cont.contestant.add(user)
        cont.save()
    except:
        cont = get_object_or_404(Contest, contest_id=contest_id)
        context = {'contest': cont, 'problem_list': cont.problems, 'part': 'Participation failed...'}
        pass
    return render(request, 'Contest.html', context)


def exit(request, contest_id):
    # 退出比赛
    try:
        cont = get_object_or_404(Contest, contest_id=contest_id)
        user = get_object_or_404(User, username=request.session['username'])
        cont.contestant.remove(user)
        context = {'contest': cont, 'problem_list': cont.problems, 'part': 'Successfully exited!'}
        cont.save()
    except:
        cont = get_object_or_404(Contest, contest_id=contest_id)
        context = {'contest': cont, 'problem_list': cont.problems, 'part': 'Exit failed...'}
        pass
    return render(request, 'Contest.html', context)


def contest_status(request, contest_id):
    # 查询出符合条件（时间在比赛时间范围内，用户为已参加比赛的用户，题目为比赛的题目）的提交
    # gt大于，gte大于等于，lt小于，lte小于等于
    contest = get_object_or_404(Contest, contest_id=contest_id)
    q = Code.objects.filter(submit_time__gte=contest.start_time).filter(submit_time__lte=contest.end_time)
    q = q.filter(problem__in=contest.problems.all())
    q = q.filter(postman__in=contest.contestant.all())
    context = {'code_list': q}
    return render(request, 'ContestStatus.html', context)


def contest_ranking(request, contest_id):
    # 比赛时的排行榜。包括：名次，用户名，通过题数、最后一题通过用时
    contest = get_object_or_404(Contest, contest_id=contest_id)  # 获取本场比赛对象
    q = Code.objects.filter(submit_time__gte=contest.start_time).filter(submit_time__lte=contest.end_time)
    q = q.filter(problem__in=contest.problems.all())
    q = q.filter(postman__in=contest.contestant.all())
    q = q.filter(AC=True)  # 找出所有已经AC的提交
    contestant = contest.contestant.all()  # 找出所有已经参加比赛的用户

    context_ls = []

    for i in contestant:
        temp_ls = []
        # 对每个已参赛的选手，找出该用户的用户名、通过题数，存在临时列表里面
        username = i.username
        accepted = q.filter(postman=i).count()
        temp_ls.append(username)
        temp_ls.append(accepted)
        # 找出他提交的题目中最晚通过的一题用时，存放在列表中
        if accepted != 0:
            latest_AC_time = q.filter(postman=i).order_by('-submit_time')[0].submit_time
            temp_ls.append(latest_AC_time-contest.start_time)
        else:
            temp_ls.append(0)
        # 添加到主列表中去
        context_ls.append(temp_ls)

    last_sorted = sorted(context_ls, key=lambda x: (-x[1], x[2]))
    context = {'context_ls': last_sorted}
    return render(request, 'ContestRanking.html', context)
