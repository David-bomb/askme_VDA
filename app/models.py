from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Профиль (1:1 с User)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Теги (M:M с Question)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Вопросы (1:M с User, M:M с Tag)
class QuestionManager(models.Manager):
    # def new(self):
    #     return self.order_by('-created_at')

    def best(self):
        # Сортировка по количеству лайков (популярные сначала)
        return self.annotate(
            total_likes=models.Count('questionlike', distinct=True),
        ).order_by('-total_likes')

    @staticmethod
    def get_popular_tags():
        return (
            Tag.objects
            .annotate(usage_count=models.Count('questions'))  # Считаем кол-во вопросов для каждого тега
            .order_by('-usage_count')  # Сортировка по убыванию
            [:7]  # Топ-7 тегов
        )



class AnswerManager(models.Manager):
    def for_question(self, question):
        return self.filter(question=question).order_by('-created_at')


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=400)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    @property
    def total_likes(self):
        return self.questionlike_set.aggregate(Sum('value'))['value__sum'] or 0

    @property
    def likes(self):
        return self.questionlike_set.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


# Ответы (1:M с User и Question)
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()

    @property
    def total_likes(self):
        return self.answerlike_set.aggregate(Sum('value'))['value__sum'] or 0

    @property
    def likes(self):
        return self.answerlike_set.count()

    def __str__(self):
        return f"Answer to: {self.question.title}"


# Лайки вопросов
class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['question']),
        ]

    @classmethod
    def update_or_create_vote(cls, user, question, value):
        obj, created = cls.objects.update_or_create(
            user=user,
            question=question,
            defaults={'value': value}
        )
        if not created and obj.value == value:
            obj.delete()
            return None
        return obj


# Лайки ответов
class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'answer')

    @classmethod
    def update_or_create_vote(cls, user, answer, value):
        obj, created = cls.objects.update_or_create(
            user=user,
            answer=answer,
            defaults={'value': value}
        )
        if not created and obj.value == value:
            obj.delete()
            return None
        return obj


