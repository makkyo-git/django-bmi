# Generated by Django 4.1.5 on 2023-03-03 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("task", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_name", models.CharField(max_length=100, verbose_name="タスク名")),
                (
                    "user_name",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="担当者名"
                    ),
                ),
                (
                    "start_date",
                    models.DateField(blank=True, null=True, verbose_name="開始日"),
                ),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="終了日"),
                ),
                (
                    "details",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="詳細"
                    ),
                ),
                (
                    "priolity",
                    models.IntegerField(
                        choices=[
                            (0, "未選択"),
                            (1, "最低"),
                            (2, "低"),
                            (3, "常"),
                            (4, "高"),
                            (5, "最高"),
                        ],
                        default=0,
                    ),
                ),
                ("update_date", models.DateField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="担当者",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectToTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "project_cd",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="task.project"
                    ),
                ),
                (
                    "task_cd",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="task.task"
                    ),
                ),
            ],
        ),
    ]
