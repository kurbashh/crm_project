# Generated by Django 5.1.2 on 2024-10-19 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0004_alter_task_deadline"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="subcategory",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="task",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("improvement_department", "Отдел благоустройства"),
                    ("municipal_department", "Отдел коммунального хозяйства"),
                    (
                        "entrepreneurship_department",
                        "Отдел по развитию предпринимательства",
                    ),
                    (
                        "infrastructure_department",
                        "Отдел инженерной и дорожной инфраструктуры",
                    ),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("not_started", "Не начато"),
                    ("in_progress", "В работе"),
                    ("done", "Завершено"),
                ],
                max_length=50,
            ),
        ),
    ]
