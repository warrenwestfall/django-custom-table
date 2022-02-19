import json
from django.core.management.base import BaseCommand, CommandError
from example_app.views import CustomMetadata


class Command(BaseCommand):

    def handle(self, *args, **options):

        # The magic line
        CustomMetadata.objects.create(
            name = "test",
            title = "Test",
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
