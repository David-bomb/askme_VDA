from app.models import Question

# Функция возврата популярных тегов. Нужно для "Popular tags" в base.html, то есть везде.
def popular_tags(request):
    return {
        'popular_tags': Question.objects.get_popular_tags()
    }

def auth_context(request):
    return {
        'is_authenticated': request.user.is_authenticated,
        'current_user': request.user
    }