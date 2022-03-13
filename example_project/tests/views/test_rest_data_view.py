import datetime
from unittest import mock
from django.utils import timezone
from decimal import Decimal
from tests.base import BaseRestSpaFormatTest
from example_app.models import RestSpaFormatMetadata, RestSpaFormatCustomTable


class RestDataViewTest(BaseRestSpaFormatTest):

    def setUp(self):
        self.setup_metadata()
        record = RestSpaFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('name', 'Robert')
        record.set_custom_value('nickname', 'Bob')
        record.set_custom_value('title', 'Bob Loblaw Law Blog')
        record.set_custom_value('status', 'Posted')
        record.set_custom_value('crm_id', 123456)
        record.set_custom_value('erp_id', 789012)
        record.set_custom_value('count', 4)
        record.set_custom_value('quantity', 17)
        record.set_custom_value('summary', 'This is the summary')
        record.set_custom_value('results', 'This is the results')
        record.set_custom_value('start_amount', 12.34)
        record.set_custom_value('end_amount', 56.789)
        record.set_custom_value('is_active', True)
        record.set_custom_value('is_superuser', False)
        record.set_custom_value('opened', datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
        record.set_custom_value('closed', datetime.datetime(2000, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))
        record.set_custom_value('list_price', Decimal('123.45'))
        record.set_custom_value('sale_price', Decimal('678.90'))
        record.set_custom_value('static_string', 'We all got this')
        record.set_custom_value('static_text', 'And this')
        mocked = datetime.datetime(2000, 4, 4, 0, 0, 0, tzinfo=datetime.timezone.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            record.save()


    def test_get_list(self):
        response = self.client.get('/rest/data/test/')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        # print(response)s
        self.assertEqual(1, len(response['rows']))
        self.assertEqual(response['columns'], [
            {"name": "name", "type": "char"},
            {"name": "nickname", "type": "char"},
            {"name": "title", "type": "char"},
            {"name": "status", "type": "char"},
            {"name": "crm_id", "type": "integer"},
            {"name": "erp_id", "type": "integer"},
            {"name": "count", "type": "integer"},
            {"name": "quantity", "type": "integer"},
            {"name": "summary", "type": "text"},
            {"name": "results", "type": "text"},
            {"name": "start_amount", "type": "float"},
            {"name": "end_amount", "type": "float"},
            {"name": "is_active", "type": "boolean"},
            {"name": "is_superuser", "type": "boolean"},
            {"name": "opened", "type": "datetime"},
            {"name": "closed", "type": "datetime"},
            {"name": "list_price", "type": "decimal-1000-2"},
            {"name": "sale_price", "type": "decimal-1000-2"},
            {"name": "id", "type": "integer", "hidden": True},
            {"name": "created", "type": "datetime"},
            {"name": "modified", "type": "datetime"},
            {"name": "static_string", "type": "char"},
            {"name": "static_text", "type": "text"},
        ])
        self.assertEqual(response['rows'][0], [
            "Robert",
            "Bob",
            "Bob Loblaw Law Blog",
            "Posted",
            123456,
            789012,
            4,
            17,
            "This is the summary",
            "This is the results",
            12.34,
            56.789,
            True,
            False,
            "2000-01-01T00:00:00Z",
            "2000-01-02T00:00:00Z",
            "123.45",
            "678.90",
            1,
            "2000-04-04T00:00:00Z",
            "2000-04-04T00:00:00Z",
            "We all got this",
            "And this",
        ])


    def test_get_record(self):
        response = self.client.get('/rest/data/test/1/')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        # print(response)
        self.assertDictEqual(response['data'], {
            "pk": 1,
            "name": "Robert",
            "nickname": "Bob",
            "title": "Bob Loblaw Law Blog",
            "status": "Posted",
            "crm_id": 123456,
            "erp_id": 789012,
            "count": 4,
            "quantity": 17,
            "summary": "This is the summary",
            "results": "This is the results",
            "start_amount": 12.34,
            "end_amount": 56.789,
            "is_active": True,
            "is_superuser": False,
            "opened": "2000-01-01T00:00:00Z",
            "closed": "2000-01-02T00:00:00Z",
            "list_price": "123.45",
            "sale_price": "678.90",
            "id": 1,
            "created": "2000-04-04T00:00:00Z",
            "modified": "2000-04-04T00:00:00Z",
            "static_string": "We all got this",
            "static_text": "And this",
        })
        self.assertDictEqual(response['metadata'], {"title": "Test",
            "type": "object",
            "properties": {
                "name": {"type": "string", "title": "Name", "maxLength": 64},
                "nickname": {"type": "string", "title": "Nickname", "maxLength": 16},
                "title": {"type": "string", "title": "Title", "maxLength": 128},
                "status": {"type": "string", "title": "Status", "maxLength": 16},
                "crm_id": {"type": "integer", "title": "CRM ID"},
                "erp_id": {"type": "integer", "title": "ERP ID"},
                "count": {"type": "integer", "title": "Count"},
                "quantity": {"type": "integer", "title": "Quantity"},
                "summary": {"type": "string", "title": "Summary", "maxLength": 1024},
                "results": {"type": "string", "title": "Results", "maxLength": 1024},
                "start_amount": {"type": "number", "title": "Start Amount"},
                "end_amount": {"type": "number", "title": "End Amount"},
                "is_active": {"type": "boolean", "title": "Is Active"},
                "is_superuser": {"type": "boolean", "title": "Is Superuser"},
                "opened": {"type": "string", "format": "date-time", "title": "Date Opened"},
                "closed": {"type": "string", "format": "date-time", "title": "Date Closed"},
                "list_price": {
                    "type": "string",
                    "format": "decimal-1000-2",
                    "title": "List Price",
                },
                "sale_price": {
                    "type": "string",
                    "format": "decimal-1000-2",
                    "title": "Sale Price",
                },
                "id": {"type": "integer", "readonly": True, "hidden": True},
                "created": {"type": "string", "format": "date-time"},
                "modified": {"type": "string", "format": "date-time"},
                "static_string": {"type": "string", "maxLength": 32},
                "static_text": {"type": "string", "maxLength": 1024},
            },
        })



    def test_post_list(self):
        post_data = {
            "name": "William",
            "nickname": "Bill",
            "title": "Billiam",
            "crm_id": 9876,
            "quantity": 192,
            "start_amount": 2.71828,
            "summary": 'This is the summary',
            "is_active": True,
            "opened": '2000-03-03T00:00:00Z',
            "list_price": '9.99',
            "static_string": 'This is the results',
            "static_text": 'This is the results',
        }     
        response = self.client.post('/rest/data/test/', post_data, 'application/json')
        self.assertEqual(response.status_code, 201)
        response = response.json()
        self.assertDictEqual(response, {
            "pk": 2,
        })
        self.assertEqual(2, RestSpaFormatCustomTable.objects.filter(metadata=self.metadata).count())
        new_record = RestSpaFormatCustomTable.objects.get(pk=2)
        self.assertEqual(new_record.get_custom_value('name'), 'William')
        self.assertEqual(new_record.get_custom_value('nickname'), 'Bill')
        self.assertEqual(new_record.get_custom_value('title'), 'Billiam')
        self.assertEqual(new_record.get_custom_value('status'), None)
        self.assertEqual(new_record.get_custom_value('crm_id'), 9876)
        self.assertEqual(new_record.get_custom_value('erp_id'), None)
        self.assertEqual(new_record.get_custom_value('count'), None)
        self.assertEqual(new_record.get_custom_value('quantity'), 192)
        self.assertEqual(new_record.get_custom_value('summary'), 'This is the summary')
        self.assertEqual(new_record.get_custom_value('results'), None)
        self.assertEqual(new_record.get_custom_value('start_amount'), 2.71828)
        self.assertEqual(new_record.get_custom_value('end_amount'), None)
        self.assertEqual(new_record.get_custom_value('is_active'), True)
        self.assertEqual(new_record.get_custom_value('is_superuser'), None)
        self.assertEqual(new_record.get_custom_value('opened'), datetime.datetime(2000, 3, 3, 0, 0, tzinfo=datetime.timezone.utc))
        self.assertEqual(new_record.get_custom_value('closed'), None)
        self.assertEqual(new_record.get_custom_value('list_price'), Decimal('9.99'))
        self.assertEqual(new_record.get_custom_value('sale_price'), None)
        self.assertEqual(new_record.get_custom_value('static_string'), 'This is the results')
        self.assertEqual(new_record.get_custom_value('static_text'), 'This is the results')


    def test_patch_title(self):
        patch_data = {
            'title': 'Gigger',
            'status': 'Giggers',
        }
        response = self.client.patch('/rest/data/test/1/', patch_data, 'application/json')
        self.assertEqual(response.status_code, 202)
        updated_record = RestSpaFormatCustomTable.objects.get(pk=1)
        self.assertEqual(updated_record.get_custom_value('name'), 'Robert')
        self.assertEqual(updated_record.get_custom_value('title'), 'Gigger')
        self.assertEqual(updated_record.get_custom_value('status'), 'Giggers')


    def test_delete(self):
        response = self.client.delete('/rest/data/test/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, RestSpaFormatCustomTable.objects.filter(metadata=self.metadata).count())
