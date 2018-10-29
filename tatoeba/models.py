from django.db import models


class Sentence(models.Model):
    tatoeba_id = models.AutoField(primary_key=True)
    lang = models.CharField(max_length=4)
    content = models.TextField()
    translation = models.ManyToManyField('Sentence', blank=True)
