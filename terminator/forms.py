from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput, )
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "email": "ایمیل",
            "username": "نام کاربری",
        }

        error_messages = {
            "username": {
                "unique": "نام کاربری تکراری است"
            },
        }

        help_texts = {
            'username': "",
        }

    # to check unique email
    def clean(self):
        super(SignUpForm, self).clean()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "ایمیل تکراری است"
            )
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = UsernameField(label="نام کاربری", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput, )

    def clean(self):
        super(LoginForm, self).clean()
        return self.cleaned_data


class ContactUsForm(forms.Form):
    title = forms.CharField(label="عنوان", )
    text = forms.CharField(label="ایمیل", widget=forms.Textarea, max_length=250, min_length=10)
    email = forms.EmailField(label="ایمیل", )