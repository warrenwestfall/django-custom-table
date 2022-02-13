import json
from django.core.management.base import BaseCommand, CommandError
from custom_table.models import Metadata


class Command(BaseCommand):

    def handle(self, *args, **options):

        # The magic line
        Metadata.objects.create(
            name = "test",
            label = "Test",
            plural = "Tests",
            storage_app_label = "example_app",
            storage_model = "examplecustomtable",
            schema = {
                "properties": {
                    "name": {
                        "type": "string",
                        "title": "Name",
                        "maxLength": 64,
                    },
                    "description": {
                        "type": "string",
                        "title": "Description",
                        "maxLength": 1024,
                    },
                }
            },
        )
