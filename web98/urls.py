"""web98 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from terminator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.signin, name="login"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('contact/', views.contact_page, name='contact-us'),
    path('contact/done', views.contact_done_page, name='contact-us-done'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit/', views.edit_profile_page, name='edit-profile'),
    # path('contact-us/', views.feedback, name='feedback'),
    # path('edit-profile/', views.update_profile, name='update_profile_success'),
    # path('contact-us/', views.feedback, name='feedback'),
]
