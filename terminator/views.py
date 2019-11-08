from itertools import chain

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from terminator.models import Course, Avatar


def index(request):
    return render(request, 'includes/base.html')


def register(request):
    user_login = request.user.is_authenticated
    # if user_login:
    #     return redirect('/profile')

    check_mail = True
    check_username = True
    check_password = True

    if (request.POST):
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        users = User.objects.all()
        for u in users:
            if u.username == username:
                check_username = False

        check_password = pass1 == pass2

        if check_mail and check_username and check_password:
            user = User.objects.create_user(username, email, pass1)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

    return render(request, 'registration/signup.html', {"user_login": user_login,
                                                        "check_mail": check_mail,
                                                        "check_username": check_username,
                                                        "check_password": check_password})


def signin(request):
    user_login = request.user.is_authenticated
    if user_login:
        return redirect('index')

    error = False
    if request.POST:
        error = True
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'registration/login.html', {"error": error})


@login_required(login_url='/')
def logout_page(request):
    logout(request)
    return redirect('index')


def contact_page(request):
    user_login = request.user.is_authenticated

    check_text_size = 0
    if request.POST:
        title = request.POST.get('title')
        email = request.POST.get('email')
        text = request.POST.get('text')
        if len(text) < 10 or len(text) > 250:
            check_text_size = -1
            return render(request, 'contact.html', {"user_login": user_login,
                                                    "check_text_size": check_text_size})
        else:
            check_text_size = 1
            text = email + "\n" + text
            send_email = EmailMessage(
                title, text, to=['webe19lopers@gmail.com']
            )
            send_email.send()
            return redirect('contact-us-done')

    return render(request, 'contact.html', {"user_login": user_login,
                                            "check_text_size": check_text_size})


def contact_done_page(request):
    return render(request, 'done.html')


def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    avatar = Avatar.objects.filter(user=user).first()
    if avatar:
        avatar_src = "/" + avatar.avatar.name
    else:
        avatar_src = ""
    return render(request, 'profile.html', {"first_name": first_name,
                                            "last_name": last_name,
                                            'username': username,
                                            'avatar': avatar_src})


def edit_profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    first_name = user.first_name
    last_name = user.last_name
    avatar = Avatar.objects.filter(user=user).first() or Avatar.objects.create(user=user)
    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        avatar_src = request.FILES.get('avatar')
        if avatar_src:
            avatar.avatar = avatar_src
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        avatar.save()
        return redirect('profile')
    else:
        return render(request, 'edit_profile.html', {'first_name': first_name,
                                                     'last_name': last_name,
                                                     'avatar': avatar.avatar})


def panel(request):
    return render(request, 'panel.html')


def create_course(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.POST:
        department = request.POST.get('department')
        name = request.POST.get('name')
        teacher = request.POST.get('teacher')
        course_number = request.POST.get('course_number')
        group_number = request.POST.get('group_number')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        first_day = request.POST.get('first_day')
        second_day = request.POST.get('second_day') or None
        course = Course(department=department,
                        name=name,
                        teacher=teacher,
                        course_number=course_number,
                        group_number=group_number,
                        start_time=start_time,
                        end_time=end_time,
                        first_day=first_day,
                        second_day=second_day,
                        )
        course.save()
    return render(request, 'create_course.html')


def search_courses(args):
    pass


def show_courses(request):
    courses = Course.objects.all()
    days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', ]
    searched_courses = None
    if request.POST:
        search_query = request.POST.get('search_query')
        department = request.POST.get('department')
        teacher = request.POST.get('teacher')
        course = request.POST.get('course')
        if not department and not teacher and not course:
            searched_courses = Course.objects.filter(department=search_query)
        else:
            if department:
                if searched_courses:
                    searched_courses = set(chain(searched_courses, Course.objects.filter(department__contains=search_query)))
                else:
                    searched_courses = Course.objects.filter(department__contains=search_query)
            if teacher:
                if searched_courses:
                    searched_courses = set(chain(searched_courses, Course.objects.filter(teacher__contains=search_query)))
                else:
                    searched_courses = Course.objects.filter(teacher__contains=search_query)
            if course:
                if searched_courses:
                    searched_courses = set(chain(searched_courses, Course.objects.filter(name__contains=search_query)))
                else:
                    searched_courses = Course.objects.filter(name__contains=search_query)
    return render(request, 'show_courses.html', {'courses': courses,
                                                 'days': days,
                                                 'search_courses': searched_courses})


def add_course(request):
    course = Course.objects.filter(id=request.GET.get('id')).first()
    course.user = request.user
    course.save()
    return redirect('courses')