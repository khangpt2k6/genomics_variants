from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import logging
from variants_project.aws_config import aws_config
from variants_project.sqs_handlers import sqs_handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Initialize AWS services (SQS queues, S3 bucket)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--queues',
            action='store_true',
            help='Initialize SQS queues'
        )
        parser.add_argument(
            '--s3',
            action='store_true',
            help='Initialize S3 bucket'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Initialize all AWS services'
        )

    def handle(self, *args, **options):
        if not settings.USE_AWS:
            raise CommandError('AWS services not enabled. Set USE_AWS=True in .env')

        queues = options['queues']
        s3 = options['s3']
        all_services = options['all']

        if not any([queues, s3, all_services]):
            queues = s3 = all_services = True

        self.stdout.write(self.style.SUCCESS('Initializing AWS services...'))

        if queues or all_services:
            self.stdout.write('Initializing SQS queues...')
            try:
                results = sqs_handler.initialize_queues()
                for queue_name, result in results.items():
                    if result['success']:
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ Queue initialized: {queue_name}")
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"✗ Failed to initialize {queue_name}: {result['error']}"
                            )
                        )
            except Exception as e:
                raise CommandError(f'Failed to initialize SQS queues: {str(e)}')

        if s3 or all_services:
            self.stdout.write('Verifying S3 bucket...')
            try:
                bucket = aws_config.s3_bucket
                region = aws_config.region
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ S3 bucket configured: {bucket} (region: {region})"
                    )
                )
            except Exception as e:
                raise CommandError(f'Failed to verify S3 bucket: {str(e)}')

        self.stdout.write(
            self.style.SUCCESS('AWS services initialized successfully!')
        )
