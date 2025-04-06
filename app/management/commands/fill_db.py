from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.db import transaction
import random
from faker import Faker
from faker.providers import internet
import datetime

fake = Faker('en_US')
fake.add_provider(internet)


class Command(BaseCommand):
    help = 'Optimized database filling with bulk operations'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Data multiplier')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # 1. Пользователи и профили
        users = User.objects.bulk_create(
            [User(
                username=fake.unique.user_name() + '_' + f'{fake.unique.random_int(min=1, max=ratio * 10)}',
                email=fake.unique.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            ) for _ in range(ratio)],
            batch_size=1000
        )

        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles, batch_size=1000)

        # 2. Теги
        tags = Tag.objects.bulk_create(
            [Tag(name=fake.word() + '_' + f'{fake.unique.random_int(min=1, max=ratio * 10)}') for _ in range(ratio)],
            batch_size=1000, ignore_conflicts=True
        )
        tags = list(Tag.objects.all())

        # 3. Вопросы с датами
        questions = Question.objects.bulk_create(
            [Question(
                author=random.choice(users),
                title=fake.sentence(),
                text=fake.text(),
                created_at=fake.date_time_between(
                    start_date='-2y',
                    end_date='now',
                    tzinfo=datetime.timezone.utc
                )
            ) for _ in range(ratio * 10)],
            batch_size=5000
        )

        # 4. Связи вопросов с тегами
        relations = []
        for question in questions:
            selected_tags = random.sample(tags, k=3)
            relations.extend([Question.tags.through(question=question, tag=tag) for tag in selected_tags])

        Question.tags.through.objects.bulk_create(
            relations,
            batch_size=10000,
            ignore_conflicts=True
        )

        # 5. Ответы с датами (не раньше даты вопроса)
        answers = []
        for _ in range(ratio * 100):
            question = random.choice(questions)
            answers.append(Answer(
                author=random.choice(users),
                question=question,
                text=fake.text(),
                is_correct=random.choice([True, False]),
                created_at=fake.date_time_between(
                    start_date=question.created_at,  # Ответ не раньше вопроса
                    end_date='now',
                    tzinfo=datetime.timezone.utc
                )
            ))

        Answer.objects.bulk_create(answers, batch_size=10000)

        # 6. Лайки вопросов
        question_likes = []
        for user in users:
            liked_questions = random.sample(questions, k=min(ratio * 200 // len(users), len(questions)))
            question_likes.extend([QuestionLike(user=user, question=q) for q in liked_questions])

        QuestionLike.objects.bulk_create(question_likes, batch_size=10000)

        # 7. Лайки ответов
        answer_likes = []
        for user in users:
            liked_answers = random.sample(answers, k=min(ratio * 200 // len(users), len(answers)))
            answer_likes.extend([AnswerLike(user=user, answer=a) for a in liked_answers])

        AnswerLike.objects.bulk_create(answer_likes, batch_size=10000)