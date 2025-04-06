from app.models import Question

# Функция возврата популярных тегов. Нужно для "Popular tags" в base.html, то есть везде.
def popular_tags(request):
    return {
        'popular_tags': Question.objects.get_popular_tags()
    }