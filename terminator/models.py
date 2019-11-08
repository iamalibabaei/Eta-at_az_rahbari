from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django import forms


class Course(models.Model):
    department = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    teacher = models.CharField(max_length=250)
    course_number = models.IntegerField()
    group_number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    first_day = models.IntegerField()
    second_day = models.IntegerField(blank=True, null=True)
    exam_date = models.DateField(null=True)
    users = models.ManyToManyField(User)


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(blank=True, null=True, upload_to='media/')


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
