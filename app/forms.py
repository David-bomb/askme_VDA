from django import forms
from django.db.models import CharField

from app.models import Profile, Question, Answer, Tag
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

    field_order = ['login', 'email', 'nickname', 'avatar']

    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите файл'
            })
        }

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['login'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email
        self.fields['nickname'].initial = self.instance.user.first_name
        # self.fields.move_to_end('avatar')

    # Проверка логина
    def clean_login(self):
        login = self.cleaned_data.get('login')
        current_login = self.instance.user.username
        if login != current_login:
            if User.objects.filter(username=login).exists() and login != current_login: # and login != user.login
                self.add_error('login', "This login is already registered")
        return login

    # Проверка email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.user.email
        if email != current_email:
            if User.objects.filter(email=email).exists() and email != current_email:# and email != user.email
                self.add_error('email', "This email is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data['login']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nickname']
        user.save()

        # Сохраняем профиль
        return super().save(commit)

class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Введите теги через пробел")

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        return [tag.strip() for tag in tags.split() if tag.strip()]

    def save(self, user, commit=True):
        question = super().save(commit=False)
        question.author = user
        if commit:
            question.save()
            self._process_tags(question)
        return question

    def _process_tags(self, question):
        for tag_name in self.cleaned_data['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)

class AnswerForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Answer
        fields = ['text']

    def save(self, user, question, commit=True):
        answer = super().save(commit=False)
        answer.author = user
        answer.question = question
        if commit:
            answer.save()
        return answer