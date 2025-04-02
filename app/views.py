from tkinter.messagebox import QUESTION

from django.core.paginator import Paginator
from django.shortcuts import HttpResponse

from django.shortcuts import render

# Create your views here.

TAGS = ['math', 'IT', 'cooking', 'promting', 'electronics', 'laws', 'sport', 'health', 'gaming', 'shopping']

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
    page = pagination(request, 5, QUESTIONS)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    page = pagination(request, 5, QUESTIONS[question_id]['answers'])
    return render(request, 'question.html', context={
        'question': QUESTIONS[question_id],
        'answers': page.object_list,  # Use paginated answers
        'page_obj': page  # Pass page_obj for pagination
    })

def hot(request):
    page = pagination(request, 5, QUESTIONS)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})
    # return HttpResponse('Hello World!')

def ask(request):
    return render(request, 'ask.html')

def tag(request, tag):
    page = pagination(request, 5, QUESTIONS)
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