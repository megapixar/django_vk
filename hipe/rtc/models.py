from django.db import models

# Create your models here.

class Chat(models.Model):
    ans = models.TextField(default='')
    offer = models.TextField(default='')
    offer_candidate = models.TextField(default='')
    answer_candidate = models.TextField(default='')

    def __unicode__(self):
        return "offer {}, answer{}, offer_candidate{}, answer_candidate{} ".format(self.offer, self.ans, self.offer_candidate, self.answer_candidate)