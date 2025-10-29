from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import logging
from variants_project.sqs_handlers import sqs_handler
from variants_project.tasks import (
    process_annotation_jobs,
    process_sync_jobs,
    process_upload_jobs
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process jobs from AWS SQS queues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--queue',
            type=str,
            choices=['annotation', 'sync', 'upload', 'all'],
            default='all',
            help='Specify which queue to process'
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='Process messages once and exit'
        )

    def handle(self, *args, **options):
        if not settings.USE_AWS:
            raise CommandError('AWS services not enabled. Set USE_AWS=True in .env')

        queue = options['queue']
        once = options['once']

        self.stdout.write(self.style.SUCCESS('Starting SQS job processor...'))

        if queue in ['annotation', 'all']:
            self.stdout.write('Processing annotation jobs...')
            result = process_annotation_jobs()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Annotation jobs: {result.get('processed', 0)} processed, "
                    f"{result.get('failed', 0)} failed"
                )
            )

        if queue in ['sync', 'all']:
            self.stdout.write('Processing sync jobs...')
            result = process_sync_jobs()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Sync jobs: {result.get('processed', 0)} processed, "
                    f"{result.get('failed', 0)} failed"
                )
            )

        if queue in ['upload', 'all']:
            self.stdout.write('Processing upload jobs...')
            result = process_upload_jobs()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Upload jobs: {result.get('processed', 0)} processed, "
                    f"{result.get('failed', 0)} failed"
                )
            )

        self.stdout.write(self.style.SUCCESS('SQS job processor completed'))
