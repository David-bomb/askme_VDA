from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy

from app.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.shortcuts import render, redirect


# Create your views here.

def pagination(request, elems_per_page, data):
    try:
        page_num = int(request.GET.get('page', 1))
        paginator = Paginator(data, elems_per_page)
        page = paginator.page(page_num)
        return page
    except Exception as e: #TODO слишком широко
        print(e)
        paginator = Paginator(data, elems_per_page)
        page = paginator.page(1)
        return page

def index(request):
    page = pagination(request, 5, Question.objects.all())
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    form = AnswerForm()
    try:
        question_obj = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return render(request, '404.html')
    answers = question_obj.answers.all().order_by('-created_at')
    page = pagination(request, 4, list(answers))

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question_obj
            answer.save()

            return redirect('question', question_id=question_id)

    return render(request, 'question.html', context={
        'question': question_obj,
        'answers': page.object_list,  # Use paginated answers
        'page_obj': page,  # Pass page_obj for pagination
        'form': form,
    })

def hot(request):
    page = pagination(request, 5, Question.objects.best())
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


@login_required(login_url=reverse_lazy('login'))
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            # Обрабатываем теги
            for tag_name in form.cleaned_data['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            return redirect('question', question_id=question.id)
    else:
        form = AskForm()

    return render(request, 'ask.html', {'form': form})

def tag(request, tag):
    tag_obj = NotImplemented
    try:
        tag_obj = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        return render(request, '404.html')
    questions = tag_obj.questions.all().order_by('-created_at')
    page = pagination(request, 5, questions)
    return render(request, 'tag.html', context={'tag': tag, 'page_obj': page, 'questions': page.object_list})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('settings'))
            else:
                form.add_error(field =None, error="User not found")
    return render(request, 'login.html', context={'form': form})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            auth.login(request, profile.user)
            return redirect(reverse('index'))
    return render(request, 'register.html', context={'form': form})

@login_required(login_url=reverse_lazy('login'))
def settings(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        raise AttributeError('Profile not found.')

    form = SettingsForm()
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        # form = SettingsForm(request.POST, profile=profile)
        if form.is_valid():
            form.save()
    return render(request, 'settings.html', context={'form': form})

@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

def Err404(request):
    return render(request, '404.html')