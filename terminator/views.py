from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.
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
            if u.email == email:
                check_mail = False

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
            # email = EmailMessage(
            # title, text, to=[email]
            # )
            # email.send()
            return redirect('contact-us-done')

    return render(request, 'contact.html', {"user_login": user_login,
                                            "check_text_size": check_text_size})


def contact_done_page(request):
    return render(request, 'done.html')