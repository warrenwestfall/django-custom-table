from tests.base import BaseRestSpaFormatTest


class MetadataRestSpaFormatModelTest(BaseRestSpaFormatTest):


    def setUp(self):
        self.static_list_metadata = [
            {
                'name': 'id',
                'type': 'integer',
                'hidden': True,
            },
            {
                'name': 'created',
                'type': 'datetime',
            },
            {
                'name': 'modified',
                'type': 'datetime',
            },
            {
                'name': 'static_string',
                'type': 'char',
            },
            {
                'name': 'static_text',
                'type': 'text',
            }
        ]
        self.static_form_properties = {
            'id': {
                'type': 'integer',
                'readonly': True,
                'hidden': True,
            },
            'created': {
                'type': 'string',
                'format': 'date-time',
            },
            'modified': {
                'type': 'string',
                'format': 'date-time',
            },
            'static_string': {
                'type': 'string',
                'maxLength': 32,
            },
            'static_text': {
                'type': 'string',
                'maxLength': 1024,
            }
        }


    def add_static_list_metadata(self, custom_list_metadata):
        return custom_list_metadata + self.static_list_metadata


    def add_static_form_metadata(self, custom_form_metadata):
        form_metadata = {
            'title': 'Test',
            'type': 'object',
            'properties': {}
        }
        form_metadata['properties'].update(custom_form_metadata)
        form_metadata['properties'].update(self.static_form_properties)
        return form_metadata


    def test_create(self):
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'name': 'ctf_char0000', 'description': 'ctf_text0000'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_char0000': 'name', 'ctf_text0000': 'description'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {'name': 'name', 'type': 'char'},
            {'name': 'description', 'type': 'text'},
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'name': {
                'type': 'string',
                'title': 'Name',
                'maxLength': 64,
            },
            'description': {
                'type': 'string',
                'title': 'Description',
                'maxLength': 1024,
            },
        }))
        self.assertEqual(metadata.get_all_field_names(),['name', 'description', 'id', 'created', 'modified', 'static_string', 'static_text'])
        self.assertEqual(metadata.get_db_field_name('name'),'ctf_char0000')
        self.assertEqual(metadata.get_db_field_name('static_string'),'static_string')


    def test_create_indexed_char(self):
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'name': 'ctf_indexed_char0000', 'nickname': 'ctf_indexed_char0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_indexed_char0000': 'name', 'ctf_indexed_char0001': 'nickname'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'name',
                'type': 'char',
            },
            {
                'name': 'nickname',
                'type': 'char',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'name': {
                'type': 'string',
                'title': 'Name',
                'maxLength': 64,
            },
            'nickname': {
                'type': 'string',
                'title': 'Nickname',
                'maxLength': 16,
            },
        }))


    def test_create_char(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'title': 'ctf_char0000', 'status': 'ctf_char0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_char0000': 'title', 'ctf_char0001': 'status'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'title',
                'type': 'char',
            },
            {
                'name': 'status',
                'type': 'char',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'title': {
                'type': 'string',
                'title': 'Title',
                'maxLength': 128,
            },
            'status': {
                'type': 'string',
                'title': 'Status',
                'maxLength': 16,
            },
        }))


    def test_create_indexed_integer(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'crm_id': 'ctf_indexed_integer0000', 'erp_id': 'ctf_indexed_integer0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_indexed_integer0000': 'crm_id', 'ctf_indexed_integer0001': 'erp_id'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'crm_id',
                'type': 'integer',
            },
            {
                'name': 'erp_id',
                'type': 'integer',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'crm_id': {
                'type': 'integer',
                "title": "CRM ID",
            },
            'erp_id': {
                'type': 'integer',
                "title": "ERP ID",
            },
        }))


    def test_create_integer(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'count': 'ctf_integer0000', 'quantity': 'ctf_integer0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_integer0000': 'count', 'ctf_integer0001': 'quantity'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'count',
                'type': 'integer',
            },
            {
                'name': 'quantity',
                'type': 'integer',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'count': {
                'type': 'integer',
                "title": "Count",
            },
            'quantity': {
                'type': 'integer',
                "title": "Quantity",
            },
        }))


    def test_create_text(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'summary': 'ctf_text0000', 'results': 'ctf_text0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_text0000': 'summary', 'ctf_text0001': 'results'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'summary',
                'type': 'text',
            },
            {
                'name': 'results',
                'type': 'text',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'summary': {
                'type': 'string',
                'title': 'Summary',
                'maxLength': 1024,
            },
            'results': {
                'type': 'string',
                'title': 'Results',
                'maxLength': 1024,
            },
        }))


    def test_create_float(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'start_amount': 'ctf_float0000', 'end_amount': 'ctf_float0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_float0000': 'start_amount', 'ctf_float0001': 'end_amount'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'start_amount',
                'type': 'float',
            },
            {
                'name': 'end_amount',
                'type': 'float',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'start_amount': {
                'type': 'number',
                'title': 'Start Amount',
            },
            'end_amount': {
                'type': 'number',
                'title': 'End Amount',
            },
        }))


    def test_create_boolean(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'is_active': 'ctf_boolean0000', 'is_superuser': 'ctf_boolean0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_boolean0000': 'is_active', 'ctf_boolean0001': 'is_superuser'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'is_active',
                'type': 'boolean',
            },
            {
                'name': 'is_superuser',
                'type': 'boolean',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'is_active': {
                'type': 'boolean',
                'title': 'Is Active',
            },
            'is_superuser': {
                'type': 'boolean',
                'title': 'Is Superuser',
            },
        }))


    def test_create_datetime(self):
        custom_data = [
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
        ]
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'opened': 'ctf_datetime0000', 'closed': 'ctf_datetime0001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_datetime0000': 'opened', 'ctf_datetime0001': 'closed'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'opened',
                'type': 'datetime',
            },
            {
                'name': 'closed',
                'type': 'datetime',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'opened': {
                'type': 'string',
                'title': 'Date Opened',
                'format': 'date-time',
            },
            'closed': {
                'type': 'string',
                'title': 'Date Closed',
                'format': 'date-time',
            },
        }))


    def test_create_decimal_1000_2(self):
        custom_data = [
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
        metadata = self.create_metadata_object(custom_data)
        self.assertEqual(metadata.custom_to_db_map, {'list_price': 'ctf_decimal-1000-20000', 'sale_price': 'ctf_decimal-1000-20001'})
        self.assertEqual(metadata.db_to_custom_map, {'ctf_decimal-1000-20000': 'list_price', 'ctf_decimal-1000-20001': 'sale_price'})
        self.assertEqual(metadata.get_custom_fields(), custom_data)
        self.assertEqual(metadata.get_list_metadata(), self.add_static_list_metadata([
            {
                'name': 'list_price',
                'type': 'decimal-1000-2',
            },
            {
                'name': 'sale_price',
                'type': 'decimal-1000-2',
            },
        ]))
        self.assertEqual(metadata.get_form_metadata(), self.add_static_form_metadata({
            'list_price': {
                'type': 'string',
                'title': 'List Price',
                'format': 'decimal-1000-2',
            },
            'sale_price': {
                'type': 'string',
                'title': 'Sale Price',
                'format': 'decimal-1000-2',
            },
        }))
