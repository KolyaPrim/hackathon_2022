from django.db import models


# Create your models here.


class UserHash(models.Model):
    user_hash = models.CharField(max_length=200)


class PollsGet(models.Model):
    poll = models.ForeignKey("your_polls.Poll", on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)