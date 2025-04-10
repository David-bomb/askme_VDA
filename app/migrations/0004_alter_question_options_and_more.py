# Generated by Django 5.2 on 2025-04-07 08:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_answer_created_at_alter_question_created_at"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="question",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="questionlike",
            index=models.Index(
                fields=["question"], name="app_questio_questio_33fcef_idx"
            ),
        ),
    ]
