from django.db import models

from custom_table.models import CustomizableMeta

class ExampleCustomTable(metaclass=CustomizableMeta):
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        app_label = 'example_app'
