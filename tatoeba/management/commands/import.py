from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from tatoeba.models import Sentence
import time
import csv


SENTENCE_BATCH_SIZE = 100000
SQL_SENTENCE_BATCH_SIZE = 1000
LINK_BATCH_SIZE = 500000
SQL_LINK_BATCH_SIZE = 1000


class Command(BaseCommand):
    help = 'Import Tatoeba sentences'

    def add_arguments(self, parser):
        parser.add_argument('--sentences', nargs='?', type=bool, default='')
        parser.add_argument('--links', nargs='?', type=bool, default='')

    def handle(self, *args, **options):
        start = time.time()

        if options['sentences']:
            with open(options['sentences']) as csvfile:
                tatoeba_reader = csv.reader(csvfile, delimiter='\t')
                sentence_list = []
                nb_sentences = 0

                # Import sentences
                for i, (s_id, lang, content) in enumerate(tatoeba_reader):
                    sentence_list.append(Sentence(
                        tatoeba_id=s_id,
                        lang=lang,
                        content=content))

                    if i % SENTENCE_BATCH_SIZE == 0:  # Batch is complete
                        self.stdout.write('Batch {:d} filled'.format(i))
                        b_start = time.time()

                        Sentence.objects.bulk_create(
                            sentence_list,
                            batch_size=SQL_SENTENCE_BATCH_SIZE,
                            ignore_conflicts=True)
                        nb_sentences += len(sentence_list)
                        sentence_list = []

                        self.stdout.write('Batch {:d} pushed [{:f}s]'.format(
                            i, time.time() - b_start))

            self.stdout.write(self.style.SUCCESS(
                '[{:.3f}s, {:d}q] Successfully imported {:d} sentences'.format(
                    time.time() - start, len(connection.queries),
                    nb_sentences)))

        sentence_ids = set([str(_id) for _id in Sentence.objects.values_list(
            'tatoeba_id', flat=True)])
        b_end = time.time()

        if options['link']:
            self.stdout.write('Start importing links')

            with open(options['link']) as csvfile:
                link_reader = csv.reader(csvfile, delimiter='\t')
                link_list = []
                # Convenient way to import m2m relationships
                # https://stackoverflow.com/a/10116452/827989
                ThroughModel = Sentence.translation.through
                nb_links = 0
                nb_defects = 0
                batch_count = 0

                # Import links
                for i, (sentence_id, translation_id) in enumerate(link_reader):
                    if (sentence_id in sentence_ids and
                            translation_id in sentence_ids):
                        batch_count += 1
                        link_list.append(ThroughModel(
                            from_sentence_id=sentence_id,
                            to_sentence_id=translation_id))
                    else:
                        nb_defects += 1

                    if batch_count == LINK_BATCH_SIZE:
                        b_start = time.time()
                        self.stdout.write('Batch {:d} filled [{:f}s]'.format(
                            i, b_start - b_end))

                        ThroughModel.objects.bulk_create(
                            link_list,
                            batch_size=SQL_LINK_BATCH_SIZE,
                            ignore_conflicts=True)
                        nb_links += len(link_list)
                        link_list = []
                        batch_count = 0

                        b_end = time.time()
                        self.stdout.write('Batch {:d} pushed [{:f}s]'.format(
                            i, b_end - b_start))

            self.stdout.write(self.style.SUCCESS(
                '[{:.3f}s, {:d}q] Successfully imported {:d} links'.format(
                    time.time() - start, len(connection.queries), nb_links)))
            self.stdout.write(self.style.SUCCESS(
                'Could not import {:d} links'.format(nb_defects)))
