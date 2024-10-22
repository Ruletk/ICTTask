# Generated by Django 4.2.6 on 2023-11-03 12:58
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_user_favorite_jobs"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
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
                ("token", models.CharField(max_length=255)),
                ("expired_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="token",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_token",
                to="account.token",
            ),
        ),
    ]
