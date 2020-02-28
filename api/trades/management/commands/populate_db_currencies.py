from django.core.management import BaseCommand

from trades.exceptions import ServiceUnavailable
from trades.utils import populate_db_currencies_from_exchange_api


class Command(BaseCommand):
    help = 'Populates the database with supported currencies from the third party API.'

    def handle(self, *args, **kwargs):
        try:
            populate_db_currencies_from_exchange_api()
        except ServiceUnavailable:
            self.stdout.write(self.style.ERROR(
                'An issue occurred while trying to populate currency from the third party API.'))
            exit(1)
        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with supported currencies.'))
