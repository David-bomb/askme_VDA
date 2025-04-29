from django import forms
from app.models import Profile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        # username = cleaned_data.get('username')
        # password = cleaned_data.get('password')
        return cleaned_data



class RegisterForm(forms.ModelForm):
    login = forms.CharField()
    email = forms.EmailField()
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['avatar']

    # Проверка логина
    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(username=login).exists():
            self.add_error('login', "This login is already registered")
        return login

    # Проверка email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['login'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['nickname']
        )
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()

        return profile


class SettingsForm(forms.ModelForm):
    login = forms.CharField()
    email = forms.EmailField()
    nickname = forms.CharField()

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        # self.profile = kwargs['profile']

    # Проверка логина
    def clean_login(self):
        login = self.cleaned_data.get('login')
        current_login = self.instance.user.username
        if login != self.instance.user.login:
            if User.objects.filter(username=login).exists() and login != current_login: # and login != user.login
                self.add_error('login', "This login is already registered")
        return login

    # Проверка email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.user.username
        if email != self.instance.user.email:
            if User.objects.filter(email=email).exists() and email != current_email:# and email != user.email
                self.add_error('email', "This email is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['login'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['nickname']
        )
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()

        return profile