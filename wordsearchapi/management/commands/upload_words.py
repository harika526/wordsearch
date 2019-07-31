import csv
from django.core.management.base import BaseCommand

from ...models import Words


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Load in TSV file of words,
        create Word objects and add them to a list
        which is then batch loaded into the database.
        """

        word_list = []

        path = r"G:\eng_word_search\wordsearch\wordsearchapi\word_search.tsv"

        print("Reading words from .tsv file...")
        reader = csv.DictReader(open(path, 'r'), fieldnames=('word', 'usage_count'))
        for row in reader:
            w = Words(
                word=row['word'],
                usage_count=row['usage_count']
            )
            word_list.append(w)

        print("Loading words to database...")

        # Batch upload our words to the database, 500 at a time
        Words.objects.bulk_create(
            word_list,
            batch_size=500
        )

        print("Done")
