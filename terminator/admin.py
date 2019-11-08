from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from terminator.models import Course

admin.site.register(Course)