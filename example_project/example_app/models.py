from django.db import models
from custom_table.models import Metadata, CustomizableMeta, CustomizableMixin
from custom_table.formats import RestSpaFormat


class CustomMetadata(Metadata):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    
    class Meta:
        app_label = 'example_app'
        format_class = RestSpaFormat()


class ExampleCustomTable(models.Model, CustomizableMixin, metaclass=CustomizableMeta):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    static_string = models.CharField('Static String', max_length=32)
    static_text = models.TextField('Static Text', max_length=1024)

    class Meta:
        metadata_model = CustomMetadata
        # custom_option = True
        app_label = 'example_app'
