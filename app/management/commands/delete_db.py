from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Очищает все данные, кроме миграций'

    def handle(self, *args, **options):
        QuestionLike.objects.all().delete()

        AnswerLike.objects.all().delete()

        Answer.objects.all().delete()

        Question.objects.all().delete()

        Tag.objects.all().delete()

        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS('База данных очищена!'))