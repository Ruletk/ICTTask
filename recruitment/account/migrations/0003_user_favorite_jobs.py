# Generated by Django 4.2.6 on 2023-11-01 16:52
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0006_rename_salary_vacancy_salary_end_and_more"),
        ("account", "0002_user_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="favorite_jobs",
            field=models.ManyToManyField(blank=True, to="jobs.vacancy"),
        ),
    ]
