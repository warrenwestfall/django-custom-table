from django.test import TestCase
from example_app.models import DefaultFormatMetadata, RestSpaFormatMetadata


class BaseDefaultFormatTest(TestCase):


    @classmethod
    def create_metadata_object(cls, custom_data):
        return DefaultFormatMetadata.objects.create(
            name = "test",
            title = "Test",
            plural = "Tests",
            storage_app_label = "example_app",
            storage_model_name = "DefaultFormatCustomTable",
            custom_data = custom_data,
        )


class BaseRestSpaFormatTest(TestCase):


    @classmethod
    def create_metadata_object(cls, custom_data):
        return RestSpaFormatMetadata.objects.create(
            name = "test",
            title = "Test",
            plural = "Tests",
            storage_app_label = "example_app",
            storage_model_name = "RestSpaFormatCustomTable",
            custom_data = custom_data,
        )
