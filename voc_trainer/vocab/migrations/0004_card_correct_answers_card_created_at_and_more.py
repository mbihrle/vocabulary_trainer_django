# Generated by Django 5.1 on 2024-08-21 20:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0003_card_stack'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='correct_answers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='card',
            name='incorrect_answers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='last_quiz_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='quiz_results',
            field=models.TextField(blank=True, null=True),
        ),
    ]
