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

    
    def setup_metadata(self):
        self.custom_data = [
            {
                "name": "name",
                "type": "indexed_char",
                "form": {
                    "title": "Name",
                    "max_length": 64,
                },
            },
            {
                "name": "nickname",
                "type": "indexed_char",
                "form": {
                    "title": "Nickname",
                    "max_length": 16,
                },
            },
            {
                "name": "title",
                "type": "char",
                "form": {
                    "title": "Title",
                    "max_length": 128,
                },
            },
            {
                "name": "status",
                "type": "char",
                "form": {
                    "title": "Status",
                    "max_length": 16,
                },
            },
            {
                "name": "crm_id",
                "type": "indexed_integer",
                "form": {
                    "title": "CRM ID",
                },
            },
            {
                "name": "erp_id",
                "type": "indexed_integer",
                "form": {
                    "title": "ERP ID",
                },
            },
            {
                "name": "count",
                "type": "integer",
                "form": {
                    "title": "Count",
                },
            },
            {
                "name": "quantity",
                "type": "integer",
                "form": {
                    "title": "Quantity",
                },
            },
            {
                "name": "summary",
                "type": "text",
                "form": {
                    "title": "Summary",
                    "max_length": 1024,
                },
            },
            {
                "name": "results",
                "type": "text",
                "form": {
                    "title": "Results",
                    "max_length": 1024,
                },
            },
            {
                "name": "start_amount",
                "type": "float",
                "form": {
                    "title": "Start Amount",
                },
            },
            {
                "name": "end_amount",
                "type": "float",
                "form": {
                    "title": "End Amount",
                },
            },
            {
                "name": "is_active",
                "type": "boolean",
                "form": {
                    "title": "Is Active",
                },
            },
            {
                "name": "is_superuser",
                "type": "boolean",
                "form": {
                    "title": "Is Superuser",
                },
            },
            {
                "name": "opened",
                "type": "datetime",
                "form": {
                    "title": "Date Opened",
                },
            },
            {
                "name": "closed",
                "type": "datetime",
                "form": {
                    "title": "Date Closed",
                },
            },
            {
                "name": "list_price",
                "type": "decimal-1000-2",
                "form": {
                    "title": "List Price",
                },
            },
            {
                "name": "sale_price",
                "type": "decimal-1000-2",
                "form": {
                    "title": "Sale Price",
                },
            },
        ]
        self.metadata = self.create_metadata_object(self.custom_data)


class BaseRestSpaFormatTest(BaseDefaultFormatTest):


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
