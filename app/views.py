from tkinter.messagebox import QUESTION

from django.core.paginator import Paginator
from django.shortcuts import HttpResponse

from django.shortcuts import render

# Create your views here.

TAGS = ['math', 'IT', 'cooking', 'promting', 'electronics', 'laws', 'sport', 'health']

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'I have {i} troubles!',
        'tags': [TAGS[i % len(TAGS)], TAGS[(i + 1) % len(TAGS)]],
        'answers': [{
            'title': f'Answer {j} for question {i}',
            'id': j,
            'text': f'I have {j} answers!',
        } for j in range(1, 10)],
    } for i in range(1, 20)
]

TAGS = ['math', 'IT', 'cooking', 'promting', 'electronics', 'laws', 'sport', 'health', 'gaming', 'shopping']

def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})
    # return HttpResponse('Hello World!')

def question(request, question_id):
    return render(request, 'question.html', context={'question': QUESTIONS[question_id],
                                                     'answers': QUESTIONS[question_id]['answers']})

def hot(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})
    # return HttpResponse('Hello World!')

def ask(request):
    return render(request, 'ask.html')

def tag(request, tag):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    tag_questions = []

    for elem in QUESTIONS:
        if tag in elem['tags']:
            tag_questions.append(elem)

    return render(request, 'tag.html', context={'tag': tag, 'page_obj': page, 'questions': tag_questions})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def settings(request):
    return render(request, 'settings.html')