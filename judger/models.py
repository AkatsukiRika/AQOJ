from django.db import models
from django.utils import timezone
import uuid
import datetime


# Create your models here.
class Problem(models.Model):
    problem_id = models.IntegerField()
    title = models.CharField(max_length=256)
    time_limit_ms = models.IntegerField()
    memory_limit_kb = models.IntegerField()
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    range_and_hint = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 有一些比赛的题目是在比赛前不能公开的，这个子段的作用就是这样
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "题目"
        verbose_name_plural = "题目"


class Code(models.Model):
    submit_time = models.DateTimeField(default=timezone.now)
    code_id = models.IntegerField(default=0)
    language = models.CharField(max_length=128)
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE)
    code_itself = models.TextField(null=True)
    # postman: 提交代码的用户。一个用户可以提交多个代码，但一份代码只能有一个提交者
    postman = models.ForeignKey('User', on_delete=models.CASCADE, default=0)
    memory_used = models.IntegerField(default=0)
    time_used = models.IntegerField(default=0)
    # 提交的代码可能有多种返回结果，这里列出来
    AC = models.BooleanField(default=False)  # Accepted
    WA = models.BooleanField(default=False)  # Wrong Answer
    TLE = models.BooleanField(default=False)  # Time Limit Exceeded
    MLE = models.BooleanField(default=False)  # Memory Limit Exceeded
    CE = models.BooleanField(default=False)  # Compile Error
    RE = models.BooleanField(default=False)  # Runtime Error
    PE = models.BooleanField(default=False)  # Presentation Error
    OLE = models.BooleanField(default=False)  # Output Limit Exceeded
    RF = models.BooleanField(default=False)  # Restricted Function
    SE = models.BooleanField(default=False)  # System Error
    WJ = models.BooleanField(default=False)  # Judging

    def __str__(self):
        return str(self.code_id)

    class Meta:
        ordering = ["-code_id"]
        verbose_name = "代码"
        verbose_name_plural = "代码"


class User(models.Model):
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    logged_in = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True)
    accepted = models.ManyToManyField(Problem)
    ac_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-ac_count"]
        verbose_name = "OJ用户"
        verbose_name_plural = "OJ用户"


class Contest(models.Model):
    # 一场比赛可以有多道题目，一道题目也可以在多场比赛中出现
    contest_id = models.IntegerField()
    title = models.CharField(max_length=256)
    problems = models.ManyToManyField(Problem)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    # 20190406更新：比赛的参赛者
    contestant = models.ManyToManyField(User)
    
    def set_active(self):
        if not self.is_active:
            if timezone.now() >= self.start_time and timezone.now() <= self.end_time:
                self.is_active = True
                self.save()
        if self.is_active:
            if timezone.now() < self.start_time or timezone.now() > self.end_time:
                self.is_active = False
                self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-contest_id"]
        verbose_name = "比赛"
        verbose_name_plural = "比赛"


class Editable(models.Model):
    # 主页的ANNOUNCEMENT和RINACHAN BOARD。前者只能管理员编辑，后者可以用户自行编辑。
    announcement = models.TextField()
    board = models.TextField()

    class Meta:
        verbose_name = "可编辑"
        verbose_name_plural = "可编辑"
