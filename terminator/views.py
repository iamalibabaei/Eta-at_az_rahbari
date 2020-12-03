from itertools import chain

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from terminator.forms import SignUpForm, LoginForm, ContactUsForm
from terminator.models import Course, Avatar, UserCourse


def index(request):
    return render(request, 'includes/base.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/profile')

    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'registration/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'registration/login.html', {"form": form})
    if request.method == "GET":
        form = LoginForm(request)
        return render(request, 'registration/login.html', {"form": form})


@login_required(login_url='/')
def logout_page(request):
    logout(request)
    return redirect('index')


def contact_page(request):
    done = False
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            title = form.cleaned_data['title']
            send_email = EmailMessage(
                subject=title, body=text, to=[email]
            )
            send_email.send()
            done = True
        return render(request, 'contact.html', {
            "form": form,
            "done": done
        })
    if request.method == "GET":
        form = ContactUsForm()
        return render(request, 'contact.html', {
            "form": form,
            "done": done
        })


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
        exam_date = request.POST.get('exam_date')
        course = Course(department=department,
                        name=name,
                        teacher=teacher,
                        course_number=course_number,
                        group_number=group_number,
                        start_time=start_time,
                        end_time=end_time,
                        first_day=first_day,
                        second_day=second_day,
                        exam_date=exam_date)
        course.save()
    return render(request, 'create_course.html')


def search_courses(args):
    pass


def show_courses(request):
    uc = UserCourse.objects.filter(user=request.user)
    my_courses = []
    my_date = []
    for u in uc:
        my_courses.append(u.course)
        my_date.append(u.course.exam_date)
    for i in my_date:
        if my_date.count(i) > 1:
            i = False
        else:
            i = True
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
                    searched_courses = set(
                        chain(searched_courses, Course.objects.filter(department__contains=search_query)))
                else:
                    searched_courses = Course.objects.filter(department__contains=search_query)
            if teacher:
                if searched_courses:
                    searched_courses = set(
                        chain(searched_courses, Course.objects.filter(teacher__contains=search_query)))
                else:
                    searched_courses = Course.objects.filter(teacher__contains=search_query)
            if course:
                if searched_courses:
                    searched_courses = set(chain(searched_courses, Course.objects.filter(name__contains=search_query)))
                else:
                    searched_courses = Course.objects.filter(name__contains=search_query)
    return render(request, 'show_courses.html', {'courses': courses,
                                                 'days': days,
                                                 'search_courses': searched_courses,
                                                 'request': request,
                                                 'uc': uc,
                                                 'my': my_courses,
                                                 'date': my_date})


def add_course(request, id):
    course = Course.objects.filter(id=id).first()
    user = request.user
    x = UserCourse.objects.filter(user=user, course=course)
    if not x:
        uc = UserCourse(user=user, course=course)
        uc.save()
        # course.delete()
    # print("XXXXXXXXXXXXXX", uc.user)
    return redirect('courses')


def delete_course(request, id):
    course = Course.objects.filter(id=id).first()
    user = request.user
    x = UserCourse.objects.filter(user=user, course=course)
    x.delete()
    return redirect('courses')


def show_course(request, id):
    course = Course.objects.filter(id=id).first()
    days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', ]
    return render(request, 'aaaaaa.html', {'course': course,
                                           'days': days})
