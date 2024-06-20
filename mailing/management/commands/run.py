from mailing.cron import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mail()
