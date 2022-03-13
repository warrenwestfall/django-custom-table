import datetime
from decimal import Decimal
from django.db import models
from tests.base import BaseDefaultFormatTest
from example_app.models import DefaultFormatCustomTable


class MetadataRestSpaFormatModelTests(BaseDefaultFormatTest):
    
    def setUp(self):
        self.setup_metadata()


    def test_create_indexed_char(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('name', 'Robert')
        record.set_custom_value('nickname', 'Bob')
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('name'), 'Robert')
        self.assertEqual(record.get_custom_value('nickname'), 'Bob')


    def test_create_char(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('title', 'Robert')
        record.set_custom_value('status', 'Started')
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('title'), 'Robert')
        self.assertEqual(record.get_custom_value('status'), 'Started')


    def test_create_indexed_integer(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('crm_id', 1234)
        record.set_custom_value('erp_id', 5678)
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('crm_id'), 1234)
        self.assertEqual(record.get_custom_value('erp_id'), 5678)


    def test_create_integer(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('count', 1234)
        record.set_custom_value('quantity', 5678)
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('count'), 1234)
        self.assertEqual(record.get_custom_value('quantity'), 5678)


    def test_create_text(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('summary', 'This is the summmary')
        record.set_custom_value('results', 'These are the results')
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('summary'), 'This is the summmary')
        self.assertEqual(record.get_custom_value('results'), 'These are the results')


    def test_create_float(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('start_amount', 123.45)
        record.set_custom_value('end_amount', 678.9)
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('start_amount'), 123.45)
        self.assertEqual(record.get_custom_value('end_amount'), 678.9)


    def test_create_boolean(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('is_active', True)
        record.set_custom_value('is_superuser', False)
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('is_active'), True)
        self.assertEqual(record.get_custom_value('is_superuser'), False)


    def test_create_datetime(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('opened', datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
        record.set_custom_value('closed', datetime.datetime(2000, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('opened'), datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
        self.assertEqual(record.get_custom_value('closed'), datetime.datetime(2000, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))


    def test_create_decimal_1000_2(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('list_price', Decimal('123.45'))
        record.set_custom_value('sale_price', Decimal('678.90'))
        record.save()
        record = DefaultFormatCustomTable.objects.get(pk=record.pk)
        self.assertEqual(record.get_custom_value('list_price'), Decimal('123.45'))
        self.assertEqual(record.get_custom_value('sale_price'), Decimal('678.90'))


    def test_field_indexed_char(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('name'))
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.db_index, True)
        self.assertEqual(field.max_length, 128)


    def test_field_char(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('title'))
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.db_index, False)
        self.assertEqual(field.max_length, 128)


    def test_field_indexed_integer(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('crm_id'))
        self.assertIsInstance(field, models.IntegerField)
        self.assertEqual(field.db_index, True)


    def test_field_integer(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('count'))
        self.assertIsInstance(field, models.IntegerField)
        self.assertEqual(field.db_index, False)


    def test_field_text(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('summary'))
        self.assertIsInstance(field, models.TextField)
        self.assertEqual(field.db_index, False)


    def test_field_float(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('start_amount'))
        self.assertIsInstance(field, models.FloatField)
        self.assertEqual(field.db_index, False)


    def test_field_boolean(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('is_active'))
        self.assertIsInstance(field, models.BooleanField)
        self.assertEqual(field.db_index, False)


    def test_field_datetime(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('opened'))
        self.assertIsInstance(field, models.DateTimeField)
        self.assertEqual(field.db_index, False)


    def test_field_decimal_1000_2(self):
        record = DefaultFormatCustomTable(metadata = self.metadata)
        field = DefaultFormatCustomTable._meta.get_field(record.metadata.get_db_field_name('list_price'))
        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.db_index, False)
        self.assertEqual(field.max_digits, 1000)
        self.assertEqual(field.decimal_places, 2)
