from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.db import transaction
from tatoeba.models import Sentence
from lapsang.models import Game
import random


class GameList(ListView):
    model = Game


class GamePrepare(DetailView):
    model = Game
    template_name = "lapsang/game_prepare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.get_object())
        print(context)
        context['lang'] = self.kwargs['lang']
        return context

    @transaction.atomic
    def post(self, *args, **kwargs):
        game = self.get_object()
        print(game)
        if self.request.POST:
            translations = {key[len('sentence_'):]: self.request.POST[key]
                            for key in self.request.POST
                            if key.startswith('sentence_')}
            for sentence_pk, content in translations.items():
                trans_pk = 1e9 + int(random.random() * 1e9)
                translation = Sentence.objects.create(tatoeba_id=trans_pk,
                                                      lang=kwargs['lang'],
                                                      content=content)
                translation.translation.add(sentence_pk)
                game.sentences.add(translation)
                Sentence.objects.get(pk=sentence_pk).translation.add(trans_pk)
            return redirect('game-detail', pk=game.pk)


class GameDetail(DetailView):
    model = Game

    def get(self, *args, **kwargs):
        game = self.get_object()
        for language in game.languages.split(','):
            if not game.is_ready(language):
                return redirect('game-prepare', pk=game.pk, lang=language)
        return super().get(*args, **kwargs)


class SentenceDetail(DetailView):
    model = Sentence


class SentenceList(ListView):
    model = Sentence
    paginate_by = 100

    def get_queryset(self):
        return Sentence.objects.filter(lang=self.kwargs['lang']).order_by('?')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def post(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        if self.request.POST:
            selected = [key[len('sentence_'):] for key in self.request.POST
                        if key.startswith('sentence_')]

            sentences = Sentence.objects.filter(tatoeba_id__in=selected)
            game = Game()
            game.save()
            game.sentences.set(sentences)

            lines = []
            for sentence in sentences:
                lines.append('{:s}::'.format(sentence.content))

            # Write to temporary file
            with open('/tmp/enfr.md', 'w') as f:
                f.write('\n'.join(lines))
            with open('/tmp/enjp.md', 'w') as f:
                f.write('\n'.join(lines))
        return render(self.request, 'tatoeba/sentence_list.html',
                      self.get_context_data(**kwargs))
