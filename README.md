# django-custom-table

# Example Usage

You first need to create a metadata model. This model is for the table to store all of the customizations users make to your customizable table. The model stores the app label and model name of the custom table model being customized, so you can have only one metadata model for mutlple customizable table models.

Edit or create an apps `models.py` module
```python
from custom_table.models import Metadata
from custom_table.formats import DefaultFormat


class MyMetadata(Metadata):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    
    class Meta:
        ct_format_class = DefaultFormat()
```

Create one or more customzable models
```python
from django.db import models
from custom_table.models import CustomizableMeta, CustomizableMixin


STORAGE_FIELDS = {
    "indexed_char": {
        "num_to_create": 10,
        "field_class": models.CharField,
        "field_class_params": {
            "max_length": 128,
            "db_index": True,
        },
    },
    "char": {
        "num_to_create": 30,
        "field_class": models.CharField,
        "field_class_params": {
            "max_length": 128,
        },
    },
    "indexed_integer": {
        "num_to_create": 20,
        "field_class": models.IntegerField,
        "field_class_params": {
            "db_index": True,
        },
    },
    "integer": {
        "num_to_create": 20,
        "field_class": models.IntegerField,
        "field_class_params": {},
    },
    "text": {
        "num_to_create": 30,
        "field_class": models.TextField,
        "field_class_params": {},
    },
    "float": {
        "num_to_create": 10,
        "field_class": models.FloatField,
        "field_class_params": {},
    },
    "boolean": {
        "num_to_create": 10,
        "field_class": models.BooleanField,
        "field_class_params": {},
    },
    "datetime": {
        "num_to_create": 10,
        "field_class": models.DateTimeField,
        "field_class_params": {},
    },
    "decimal-1000-2": {
        "num_to_create": 10,
        "field_class": models.DecimalField,
        "field_class_params": {
            "max_digits": 1000,
            "decimal_places": 2,
        },
    },
}


class MyCustomTable(models.Model, CustomizableMixin, metaclass=CustomizableMeta):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    static_string = models.CharField('Static String', max_length=32)
    static_text = models.TextField('Static Text', max_length=1024)

    class Meta:
        ct_metadata_model = MyMetadata
        ct_storage_fields = STORAGE_FIELDS
```


If you require your own form and/or list metadata formats you can create your own metadata format class
```python
from custom_table.formats import BaseFormat


class RestSpaFormat(BaseFormat):
    """ Format metadata for use in a Single Page App with a REST back end
        and a Javascript front end
        Form metadate follows react-jsonschema-form
    """

    def get_list_metadata(self, metadata):
        all_fields = self.get_all_fields(metadata)
        # print(all_fields)
        list_metadata = []
        for field in all_fields:
            type = field['type']
            if type.startswith('indexed_'):
                type = type[8:]
            list_field = {
                'name': field['name'],
                'type': type,
            }
            if 'list' in field:
                for list_property, value in field['list'].items():
                    list_field[list_property] = value
            list_metadata.append(list_field)
        return list_metadata


    def get_form_metadata(self, metadata):
        all_fields = self.get_all_fields(metadata)
        form_metadata = {
            'title': metadata.title,
            'type': 'object',
            'properties': {},
        }
        for field in all_fields:
            properties = {
                'type': field['type'],
            }
            if field['type'] in ('indexed_char', 'char', 'text',):
                properties['type'] = 'string'
            if field['type'] in ('indexed_integer', 'integer',):
                properties['type'] = 'integer'
            if field['type'] == 'float':
                properties['type'] = 'number'
            if field['type'] == 'datetime':
                properties['type'] = 'string'
                properties['format'] = 'date-time'
            if field['type'].startswith('decimal'):
                # _, max_digits, decimal_places = field['type'].split('_')
                properties['type'] = 'string'
                properties['format'] = field['type']
            if 'form' in field:
                for form_property, value in field['form'].items():
                    properties[snake_to_camel(form_property)] = value
            form_metadata['properties'][field['name']] = properties
        return form_metadata
```
The above example is taken from the built in django-custom-table formats and can be used as is as follows
```python
from custom_table.formats import RestSpaFormat
```
