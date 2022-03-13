from django.urls import reverse
from tests.base import BaseRestSpaFormatTest
from example_app.models import RestSpaFormatMetadata, RestSpaFormatCustomTable


class RestMetadataViewTest(BaseRestSpaFormatTest):

    def setUp(self):
        self.setup_metadata()


    def test_get_list(self):
        response = self.client.get('/rest/metadata/')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(1, len(response))
        self.assertDictEqual(response[0], {
            "name": "test",
            "title": "Test",
            "plural": "Tests",
            "storage_app_label": "example_app",
            "storage_model_name": "RestSpaFormatCustomTable",
            "custom_data": self.custom_data,
        })


    def test_get_record(self):
        response = self.client.get('/rest/metadata/test/')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        # print(response)
        self.assertEqual(response['name'], 'test')
        self.assertEqual(response['title'], 'Test')
        self.assertEqual(response['plural'], 'Tests')
        self.assertEqual(response['storage_app_label'], 'example_app')
        self.assertEqual(response['storage_model_name'], 'RestSpaFormatCustomTable')
        self.assertEqual(response['custom_data'], self.custom_data)
        self.assertEqual(response['list_metadata'], [
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
        self.assertEqual(response['form_metadata'], {
            "title": "Test",
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


    def test_get_record_by_id(self):
        response = self.client.get('/rest/metadata/1/')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        # print(response)
        self.assertEqual(response['name'], 'test')
        self.assertEqual(response['title'], 'Test')
        self.assertEqual(response['plural'], 'Tests')
        self.assertEqual(response['storage_app_label'], 'example_app')
        self.assertEqual(response['storage_model_name'], 'RestSpaFormatCustomTable')
        self.assertEqual(response['custom_data'], self.custom_data)
        self.assertEqual(response['list_metadata'], [
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
        self.assertEqual(response['form_metadata'], {
            "title": "Test",
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
            "name": "thing",
            "title": "Thing",
            "plural": "Things",
            "storage_app_label": "example_app",
            "storage_model_name": "RestSpaFormatCustomTable",
            "custom_data": self.custom_data,
        }
        response = self.client.post('/rest/metadata/', post_data, 'application/json')
        self.assertEqual(response.status_code, 201)
        response = response.json()
        self.assertDictEqual(response, {
            "pk": 2,
        })
        self.assertEqual(2, RestSpaFormatMetadata.objects.all().count())
        new_record = RestSpaFormatMetadata.objects.get(pk=2)
        self.assertEqual(new_record.name, 'thing')
        self.assertEqual(new_record.title, 'Thing')
        self.assertEqual(new_record.plural, 'Things')
        self.assertEqual(new_record.storage_app_label, 'example_app')
        self.assertEqual(new_record.storage_model_name, 'RestSpaFormatCustomTable')
        self.assertEqual(new_record.custom_data, self.custom_data)
        self.assertDictEqual(new_record.custom_to_db_map, {
            "name": "ctf_indexed_char0000",
            "nickname": "ctf_indexed_char0001",
            "title": "ctf_char0000",
            "status": "ctf_char0001",
            "crm_id": "ctf_indexed_integer0000",
            "erp_id": "ctf_indexed_integer0001",
            "count": "ctf_integer0000",
            "quantity": "ctf_integer0001",
            "summary": "ctf_text0000",
            "results": "ctf_text0001",
            "start_amount": "ctf_float0000",
            "end_amount": "ctf_float0001",
            "is_active": "ctf_boolean0000",
            "is_superuser": "ctf_boolean0001",
            "opened": "ctf_datetime0000",
            "closed": "ctf_datetime0001",
            "list_price": "ctf_decimal-1000-20000",
            "sale_price": "ctf_decimal-1000-20001",
        })
        self.assertDictEqual(new_record.db_to_custom_map, {
            "ctf_indexed_char0000": "name",
            "ctf_indexed_char0001": "nickname",
            "ctf_char0000": "title",
            "ctf_char0001": "status",
            "ctf_indexed_integer0000": "crm_id",
            "ctf_indexed_integer0001": "erp_id",
            "ctf_integer0000": "count",
            "ctf_integer0001": "quantity",
            "ctf_text0000": "summary",
            "ctf_text0001": "results",
            "ctf_float0000": "start_amount",
            "ctf_float0001": "end_amount",
            "ctf_boolean0000": "is_active",
            "ctf_boolean0001": "is_superuser",
            "ctf_datetime0000": "opened",
            "ctf_datetime0001": "closed",
            "ctf_decimal-1000-20000": "list_price",
            "ctf_decimal-1000-20001": "sale_price",
        })


    def test_patch_title(self):
        patch_data = {
            'title': 'Gigger',
            'plural': 'Giggers',
        }
        response = self.client.patch('/rest/metadata/test/', patch_data, 'application/json')
        self.assertEqual(response.status_code, 202)
        updated_record = RestSpaFormatMetadata.objects.get(pk=1)
        self.assertEqual(updated_record.name, 'test')
        self.assertEqual(updated_record.title, 'Gigger')
        self.assertEqual(updated_record.plural, 'Giggers')


    def test_patch_title_by_id(self):
        patch_data = {
            'title': 'Gigger',
            'plural': 'Giggers',
        }
        response = self.client.patch('/rest/metadata/1/', patch_data, 'application/json')
        self.assertEqual(response.status_code, 202)
        updated_record = RestSpaFormatMetadata.objects.get(pk=1)
        self.assertEqual(updated_record.name, 'test')
        self.assertEqual(updated_record.title, 'Gigger')
        self.assertEqual(updated_record.plural, 'Giggers')


    def test_patch_add_indexed_char(self):
        record = RestSpaFormatCustomTable(metadata = self.metadata)
        record.set_custom_value('name', 'Robert')
        record.set_custom_value('nickname', 'Bob')
        record.save()
        self.custom_data.append({
            "name": "code",
            "type": "indexed_char",
            "form": {
                "title": "Code",
                "max_length": 64,
            },
        })
        patch_data = {
            'custom_data': self.custom_data,
        }
        response = self.client.patch('/rest/metadata/test/', patch_data, 'application/json')
        self.assertEqual(response.status_code, 202)
        updated_record = RestSpaFormatMetadata.objects.get(pk=1)
        self.assertEqual(updated_record.name, 'test')
        self.assertEqual(updated_record.custom_data,  self.custom_data)
        self.assertDictEqual(updated_record.custom_to_db_map, {
            "name": "ctf_indexed_char0000",
            "nickname": "ctf_indexed_char0001",
            "title": "ctf_char0000",
            "status": "ctf_char0001",
            "crm_id": "ctf_indexed_integer0000",
            "erp_id": "ctf_indexed_integer0001",
            "count": "ctf_integer0000",
            "quantity": "ctf_integer0001",
            "summary": "ctf_text0000",
            "results": "ctf_text0001",
            "start_amount": "ctf_float0000",
            "end_amount": "ctf_float0001",
            "is_active": "ctf_boolean0000",
            "is_superuser": "ctf_boolean0001",
            "opened": "ctf_datetime0000",
            "closed": "ctf_datetime0001",
            "list_price": "ctf_decimal-1000-20000",
            "sale_price": "ctf_decimal-1000-20001",
            "code": "ctf_indexed_char0002",
        })
        self.assertDictEqual(updated_record.db_to_custom_map, {
            "ctf_indexed_char0000": "name",
            "ctf_indexed_char0001": "nickname",
            "ctf_char0000": "title",
            "ctf_char0001": "status",
            "ctf_indexed_integer0000": "crm_id",
            "ctf_indexed_integer0001": "erp_id",
            "ctf_integer0000": "count",
            "ctf_integer0001": "quantity",
            "ctf_text0000": "summary",
            "ctf_text0001": "results",
            "ctf_float0000": "start_amount",
            "ctf_float0001": "end_amount",
            "ctf_boolean0000": "is_active",
            "ctf_boolean0001": "is_superuser",
            "ctf_datetime0000": "opened",
            "ctf_datetime0001": "closed",
            "ctf_decimal-1000-20000": "list_price",
            "ctf_decimal-1000-20001": "sale_price",
            "ctf_indexed_char0002": "code",
        })
        response = self.client.get('/rest/data/test/1/')
        response = response.json()
        self.assertEqual(response['data']['name'], 'Robert')
        self.assertEqual(response['data']['nickname'], 'Bob')
        self.assertEqual(response['data']['code'], None)
        record = RestSpaFormatCustomTable.objects.get(id=1)
        record.set_custom_value('code', 'HR123')
        record.save()
        response = self.client.get('/rest/data/test/1/')
        response = response.json()
        self.assertEqual(response['data']['name'], 'Robert')
        self.assertEqual(response['data']['nickname'], 'Bob')
        self.assertEqual(response['data']['code'], 'HR123')


    def test_delete(self):
        response = self.client.delete('/rest/metadata/test/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, RestSpaFormatMetadata.objects.all().count())


    def test_delete_by_id(self):
        response = self.client.delete('/rest/metadata/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, RestSpaFormatMetadata.objects.all().count())
