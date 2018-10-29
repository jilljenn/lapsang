from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from tatoeba.models import Sentence


class SentenceDetail(DetailView):
    model = Sentence


class SentenceList(ListView):
    model = Sentence
    paginate_by = 50

    def get_queryset(self):
        return Sentence.objects.filter(lang=self.kwargs['lang']).order_by('?')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def post(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        if self.request.POST:
            selected = [key[len('sentence_'):] for key in self.request.POST
                        if key.startswith('sentence_')]
            lines = []
            for sentence in Sentence.objects.filter(tatoeba_id__in=selected):
                lines.append('{:s}::'.format(sentence.content))
            with open('/tmp/enfr.md', 'w') as f:
                f.write('\n'.join(lines))
            with open('/tmp/enjp.md', 'w') as f:
                f.write('\n'.join(lines))
        return render(self.request, 'tatoeba/sentence_list.html',
                      self.get_context_data(**kwargs))
