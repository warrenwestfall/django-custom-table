import json
from django.core.management.base import BaseCommand, CommandError
from example_app.views import RestSpaFormatMetadata


class Command(BaseCommand):

    def handle(self, *args, **options):
        RestSpaFormatMetadata.objects.create(
            name = "test",
            title = "Test",
            plural = "Tests",
            storage_app_label = "example_app",
            storage_model_name = "RestSpaFormatCustomTable",
            custom_data = [
                {
                    "name": "name",
                    "type": "char",
                    "form": {
                        "title": "Name",
                        "max_length": 64,
                    },
                },
                {
                    "name": "description",
                    "type": "text",
                    "form": {
                        "title": "Description",
                        "max_length": 1024,
                    },
                },
            ],
        )
