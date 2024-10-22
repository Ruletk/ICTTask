# Generated by Django 4.2.6 on 2023-11-18 17:30
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jobs", "0009_rename_salary_end_vacancy_salary_max_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="published_at",
            field=models.DateTimeField(),
        ),
    ]
