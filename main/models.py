from django.db import models


class Tests(models.Model):
    name = models.CharField('name', max_length=255)
    number_questions = models.IntegerField('number_questions')
    questions_options = models.TextField('questions_options')
    correct_answers = models.TextField('correct_answers')

    def __str__(self):
        return f"{self.name} - {self.number_questions} вопросов"

