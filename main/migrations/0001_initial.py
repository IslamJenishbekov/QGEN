# Generated by Django 5.1.4 on 2025-01-13 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('number_questions', models.IntegerField(verbose_name='number_questions')),
                ('questions_options', models.TextField(verbose_name='questions_options')),
                ('correct_answers', models.TextField(verbose_name='correct_answers')),
            ],
        ),
    ]
