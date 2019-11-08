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
