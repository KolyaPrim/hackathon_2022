from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime

# Create your models here.
User = get_user_model()


class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    css_file = models.FileField(upload_to='polls_styles/', default='')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    token = models.CharField(max_length=200)


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    value = models.TextField(blank=True)
    name = models.CharField(max_length=50, blank=True)


class Answer(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    value = models.TextField()
