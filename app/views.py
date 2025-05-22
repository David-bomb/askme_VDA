from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404  # Добавлен импорт
from django.views.decorators.http import require_POST

from app.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.shortcuts import render, redirect


def pagination(request, elems_per_page, data):
    try:
        page_num = int(request.GET.get('page', 1))
        paginator = Paginator(data, elems_per_page)
        page = paginator.page(page_num)
        return page
    except (PageNotAnInteger, EmptyPage):
        paginator = Paginator(data, elems_per_page)
        page = paginator.page(1)
        return page


def index(request):
    page = pagination(request, 5, Question.objects.all())
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    form = AnswerForm()
    question_obj = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.for_question(question_obj)
    page = pagination(request, 4, answers)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(user=request.user, question=question_obj)

            return redirect('question', question_id=question_id)

    return render(request, 'question.html', context={
        'question': question_obj,
        'answers': page.object_list,
        'page_obj': page,
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
            question = form.save(user=request.user)

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
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))  # Редирект для обновления данных
    else:
        form = SettingsForm(instance=profile)
    return render(request, 'settings.html', context={'form': form})


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

def Err404(request):
    return render(request, '404.html')


@require_POST
@login_required
def like_async(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
        action = request.POST.get('action')  # 'like' или 'dislike'
        value = 1 if action == 'like' else -1

        # Обновить или создать запись
        QuestionLike.update_or_create_vote(
            user=request.user,
            question=question,
            value=value
        )

        # Пересчитать общий рейтинг вопроса
        total_likes = QuestionLike.objects.filter(question=question).aggregate(
            Sum('value')
        )['value__sum'] or 0

        return JsonResponse({'total_likes': total_likes})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@login_required
def answer_like_async(request, answer_id):
    try:
        answer = get_object_or_404(Answer, id=answer_id)
        action = request.POST.get('action')  # 'like' или 'dislike'
        value = 1 if action == 'like' else -1

        AnswerLike.update_or_create_vote(
            user=request.user,
            answer=answer,
            value=value
        )

        answer.refresh_from_db()
        return JsonResponse({'total_likes': answer.total_likes})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@login_required
def mark_answer_correct(request, answer_id):
    try:
        answer = get_object_or_404(Answer, id=answer_id)
        if request.user != answer.question.author:
            return JsonResponse({'error': 'Only question author can mark answers'}, status=403)

        # Инвертируем значение is_correct
        answer.is_correct = not answer.is_correct
        answer.save()
        return JsonResponse({'is_correct': answer.is_correct})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)