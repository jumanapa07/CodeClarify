# Generated by Django 5.0.3 on 2024-03-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeclarify', '0006_rename_difficulty_problem_difficulty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
