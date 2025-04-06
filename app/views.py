from django.core.paginator import Paginator
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.shortcuts import render

# Create your views here.

def pagination(request, elems_per_page, data):
    try:
        page_num = int(request.GET.get('page', 1))
        paginator = Paginator(data, elems_per_page)
        page = paginator.page(page_num)
        return page
    except Exception as e:
        print(e)
        paginator = Paginator(data, elems_per_page)
        page = paginator.page(1)
        return page

def index(request):
    page = pagination(request, 5, Question.objects.all())
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    question_obj = Question.objects.get(id=question_id)
    answers = question_obj.answers.all().order_by('-created_at')
    page = pagination(request, 4, list(answers))
    return render(request, 'question.html', context={
        'question': question_obj,
        'answers': page.object_list,  # Use paginated answers
        'page_obj': page  # Pass page_obj for pagination
    })

def hot(request):
    page = pagination(request, 5, Question.objects.best())
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})

def ask(request):
    return render(request, 'ask.html')

def tag(request, tag):
    tag_obj = Tag.objects.get(name=tag)
    questions = tag_obj.questions.all().order_by('-created_at')
    page = pagination(request, 5, questions)

    return render(request, 'tag.html', context={'tag': tag, 'page_obj': page, 'questions': page.object_list})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def settings(request):
    return render(request, 'settings.html')