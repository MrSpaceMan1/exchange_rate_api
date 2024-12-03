from django.core.management import BaseCommand
from . import _fetch

class Command(BaseCommand):
    help = "Fetches exchange data and saves it to database"

    def handle(self, *args, **options):
        _fetch.fetch(self)
