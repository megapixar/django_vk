from django.db import models

# Create your models here.

class Chat(models.Model):
    offer = models.TextField()
    answer = models.TextField()
    offer_candidate = models.TextField(default='')
    answer_candidate = models.TextField(default='')