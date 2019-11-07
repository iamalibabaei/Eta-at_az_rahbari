from django.contrib.auth.models import User
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
        firstname = request.POST.get('first-name')
        lastname = request.POST.get('last-name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

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

            # user_profile = UserProfile()
            # user_profile.user = user
            # user_profile.userID = user.id
            # user_profile.save()

            return redirect('/')

    return render(request, 'signup.html', {"user_login": user_login,
                                           "check_mail": check_mail,
                                           "check_username": check_username,
                                           "check_password": check_password})

