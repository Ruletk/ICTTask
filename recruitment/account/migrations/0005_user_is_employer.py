# Generated by Django 4.2.6 on 2023-11-03 18:19
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_token_user_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_employer",
            field=models.BooleanField(default=False),
        ),
    ]