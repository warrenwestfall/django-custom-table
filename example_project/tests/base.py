from django.test import TestCase
from example_app.models import CustomMetadata


class BaseCustomTableTest(TestCase):


    @classmethod
    def create_metadata_object(cls, custom_data):
        return CustomMetadata.objects.create(
            name = "test",
            title = "Test",
            plural = "Tests",
            storage_app_label = "example_app",
            storage_model_name = "examplecustomtable",
            custom_data = custom_data,
        )
