from django.db import models

from custom_table.models import Metadata, CustomizableMeta, CustomizableMixin

class CustomMetadata(Metadata):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)
    
    class Meta:
        app_label = 'example_app'


class ExampleCustomTable(models.Model, CustomizableMixin, metaclass=CustomizableMeta):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        metadata_model = CustomMetadata
        app_label = 'example_app'
