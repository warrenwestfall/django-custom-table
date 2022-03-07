import datetime
from decimal import Decimal
from django.db import models
from tests.base import BaseCustomTableTest
from example_app.models import ExampleCustomTable


class MetadataRestSpaFormatModelTests(BaseCustomTableTest):
    
    def setUp(self):
        custom_data = [
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
        self.metadata = self.create_metadata_object(custom_data)


    def test_create_indexed_char(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('name', 'Robert')
        record.set_custom_value('nickname', 'Bob')
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('name'), 'Robert')
        self.assertEqual(record.get_custom_value('nickname'), 'Bob')


    def test_create_char(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('title', 'Robert')
        record.set_custom_value('status', 'Started')
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('title'), 'Robert')
        self.assertEqual(record.get_custom_value('status'), 'Started')


    def test_create_indexed_integer(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('crm_id', 1234)
        record.set_custom_value('erp_id', 5678)
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('crm_id'), 1234)
        self.assertEqual(record.get_custom_value('erp_id'), 5678)


    def test_create_integer(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('count', 1234)
        record.set_custom_value('quantity', 5678)
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('count'), 1234)
        self.assertEqual(record.get_custom_value('quantity'), 5678)


    def test_create_text(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('summary', 'This is the summmary')
        record.set_custom_value('results', 'These are the results')
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('summary'), 'This is the summmary')
        self.assertEqual(record.get_custom_value('results'), 'These are the results')


    def test_create_float(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('start_amount', 123.45)
        record.set_custom_value('end_amount', 678.9)
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('start_amount'), 123.45)
        self.assertEqual(record.get_custom_value('end_amount'), 678.9)


    def test_create_boolean(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('is_active', True)
        record.set_custom_value('is_superuser', False)
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('is_active'), True)
        self.assertEqual(record.get_custom_value('is_superuser'), False)


    def test_create_datetime(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('opened', datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
        record.set_custom_value('closed', datetime.datetime(2000, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('opened'), datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
        self.assertEqual(record.get_custom_value('closed'), datetime.datetime(2000, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))


    def test_create_decimal_1000_2(self):
        record = ExampleCustomTable(metadata = self.metadata)
        record.set_custom_value('list_price', Decimal('123.45'))
        record.set_custom_value('sale_price', Decimal('678.90'))
        record.save()
        record = ExampleCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('list_price'), Decimal('123.45'))
        self.assertEqual(record.get_custom_value('sale_price'), Decimal('678.90'))


    def test_field_indexed_char(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('name'))
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.db_index, True)
        self.assertEqual(field.max_length, 128)


    def test_field_char(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('title'))
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.db_index, False)
        self.assertEqual(field.max_length, 128)


    def test_field_indexed_integer(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('crm_id'))
        self.assertIsInstance(field, models.IntegerField)
        self.assertEqual(field.db_index, True)


    def test_field_integer(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('count'))
        self.assertIsInstance(field, models.IntegerField)
        self.assertEqual(field.db_index, False)


    def test_field_text(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('summary'))
        self.assertIsInstance(field, models.TextField)
        self.assertEqual(field.db_index, False)


    def test_field_float(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('start_amount'))
        self.assertIsInstance(field, models.FloatField)
        self.assertEqual(field.db_index, False)


    def test_field_boolean(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('is_active'))
        self.assertIsInstance(field, models.BooleanField)
        self.assertEqual(field.db_index, False)


    def test_field_datetime(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('opened'))
        self.assertIsInstance(field, models.DateTimeField)
        self.assertEqual(field.db_index, False)


    def test_field_decimal_1000_2(self):
        record = ExampleCustomTable(metadata = self.metadata)
        field = ExampleCustomTable._meta.get_field(record.metadata.get_db_field_name('list_price'))
        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.db_index, False)
        self.assertEqual(field.max_digits, 1000)
        self.assertEqual(field.decimal_places, 2)
