from django.db import models
from tatoeba.models import Sentence
from collections import Counter


class Game(models.Model):
    sentences = models.ManyToManyField(Sentence)
    time = models.DateTimeField(auto_now=True)
    languages = models.CharField(max_length=16, default='fra,jpn')

    def is_ready(self, lang):
        nb_sentences = Counter(self.sentences.values_list('lang', flat=True))
        return nb_sentences[lang] == nb_sentences['eng']

    def get_eng_sentences(self):
        return self.sentences.filter(lang='eng')

    def get_play_sentences(self):
        sentences = list(self.sentences.exclude(lang='eng')
                                       .order_by('lang', '?'))
        nb_sentences = len(sentences)
        return [item for pair in zip(sentences[:nb_sentences // 2],
                                     sentences[nb_sentences // 2:]) for item in pair]

    def nb_sentences(self):
        return self.sentences.exclude(lang='eng').count()
