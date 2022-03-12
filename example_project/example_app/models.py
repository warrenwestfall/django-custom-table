from django.db import models
from custom_table.models import Metadata, CustomizableMeta, CustomizableMixin
from custom_table.formats import DefaultFormat, RestSpaFormat


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


class DefaultFormatMetadata(Metadata):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    
    class Meta:
        app_label = 'example_app'
        ct_format_class = DefaultFormat()


class DefaultFormatCustomTable(models.Model, CustomizableMixin, metaclass=CustomizableMeta):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    static_string = models.CharField('Static String', max_length=32)
    static_text = models.TextField('Static Text', max_length=1024)

    class Meta:
        ct_metadata_model = DefaultFormatMetadata
        app_label = 'example_app'
        ct_storage_fields = STORAGE_FIELDS


class RestSpaFormatMetadata(Metadata):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    
    class Meta:
        app_label = 'example_app'
        ct_format_class = RestSpaFormat()


class RestSpaFormatCustomTable(models.Model, CustomizableMixin, metaclass=CustomizableMeta):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    static_string = models.CharField('Static String', max_length=32)
    static_text = models.TextField('Static Text', max_length=1024)

    class Meta:
        ct_metadata_model = RestSpaFormatMetadata
        app_label = 'example_app'
        ct_storage_fields = STORAGE_FIELDS
