from django.core.management.base import BaseCommand, CommandError
from note.models import Notes
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        if Notes.objects.get(delete_note=True):
            Notes.objects.filter(reminder=datetime.now()-timedelta(days=7)).delete()
            self.stdout.write('Deleted objects older than 7 days')