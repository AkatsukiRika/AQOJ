"""JUDGE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from judger import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^JudgeHome/', views.judge_home),
    re_path(r'^ProblemSet/', views.problem_set),
    re_path(r'^Problem/(?P<problem_id>[0-9]+)/$', views.problem, name='problem'),
    re_path(r'^Submitted/(?P<problem_id>[0-9]+)/$', views.submit_code, name='submit_code'),
    re_path(r'^Register/', views.register, name='register'),
    re_path(r'^Login/', views.login, name='login'),
    re_path(r'^Logout/', views.logout),
    re_path(r'^Status/', views.status, name='status'),
    re_path(r'^ContestList/', views.contest_list),
    re_path(r'^Contest/(?P<contest_id>[0-9]+)/$', views.contest, name='contest'),
    re_path(r'^Ranking/', views.ranking),
    re_path(r'^Contest/(?P<contest_id>[0-9]+)/participated/$', views.participate, name='participate'),
    re_path(r'^Contest/(?P<contest_id>[0-9]+)/exited/$', views.exit, name='exit'),
    re_path(r'^ContestStatus/(?P<contest_id>[0-9]+)/$', views.contest_status),
    re_path(r'^ContestRanking/(?P<contest_id>[0-9]+)/$', views.contest_ranking)
]
