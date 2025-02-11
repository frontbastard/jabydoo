import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Waits for database to be available"  # noqa: VNE003

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        max_retries = 30
        retry_count = 0
        while not db_conn and retry_count < max_retries:
            try:
                db_conn = connections["default"]
            except OperationalError:
                retry_count += 1
                self.stdout.write(f"Database unavailable, retrying {retry_count}/{max_retries}...")
                time.sleep(2)

        if db_conn:
            self.stdout.write(self.style.SUCCESS("Database available!"))
        else:
            self.stdout.write(self.style.ERROR("Database not available after several retries!"))
