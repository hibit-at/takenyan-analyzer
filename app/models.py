from django.db import models

# Create your models here.

class Tweet(models.Model):
    tw_id = models.CharField(default='',max_length=280)
    dt = models.DateTimeField()
    usr = models.CharField(default='',max_length=280)
    txt = models.CharField(default='',max_length=280)
