import time

from django.core.management.base import BaseCommand

from apps.schedule.utils import update_schedule

SLEEP_TIME = 60 * 60 * 12


class Command(BaseCommand):
    help = 'Updates schedule from Mospolytech Server'

    def handle(self, *args, **options):
        while True:
            update_schedule()
            self.stdout.write(self.style.SUCCESS('Successfully parsed'))
            time.sleep(SLEEP_TIME)
