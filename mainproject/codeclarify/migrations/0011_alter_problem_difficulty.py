# Generated by Django 5.0.3 on 2024-04-07 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeclarify', '0010_problem_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=10),
        ),
    ]
