import json
from copy import deepcopy
from django.apps import apps
from django.db import transaction
from django.db import models
from django.conf import settings
from django.apps import apps


class MetadataFields(models.Model):
    name = models.CharField("Table Name", max_length=64, db_index=True, unique=True)
    title = models.CharField("Title", max_length=128)
    plural = models.CharField("Plural Title", max_length=128)
    storage_app_label = models.CharField("Database Table Name", max_length=64)
    storage_model = models.CharField("Database Table Name", max_length=64)
    schema = models.JSONField("Schema Data", default=dict)
    db_fields = models.JSONField("Database Fields", default=dict, blank=True)
    field_map = models.JSONField("Field Map", default=dict, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        abstract = True
        index_together = (
            ('storage_app_label', 'storage_model')
        )


class Metadata(MetadataFields):

    class Meta:
        abstract = True
        app_label = 'custom_table'


    def __str__(self):
        return self.name


    @transaction.atomic
    def save(self, *args, **kwargs):
        self._update_db_fields()
        super(Metadata, self).save(*args, **kwargs)
        self._create_view()


    def get_storage_model(self):
        return apps.get_model(self.storage_app_label, self.storage_model)


    def _update_db_fields(self):
        from custom_table.models.customizable import DATA_TYPES, db_field_name, db_field_type
        next_nums = { type_name:0 for type_name in DATA_TYPES.keys() }
        for field, db_field in self.db_fields.items():
            type, current_num = db_field_type(db_field)
            if current_num >= next_nums[type]:
                next_nums[type] = current_num + 1
        for field, property in self.schema['properties'].items():
            type = property['type']
            if property['type'] == 'string':
                if 'maxLength' in property and property['maxLength'] <= 128:
                    type = 'char'
                else:
                    type = 'text'
            if field not in self.db_fields:
                self.db_fields[field] = db_field_name(type, next_nums[type])
                next_nums[type] += 1


    def _create_view(self):
        from django.db import connection
        storage_model = self.get_storage_model()
        cur = connection.cursor()
        view_name = '{}_v'.format(self.name)
        sql = 'drop view if exists {}'.format(view_name)
        cur.execute(sql, [])
        sql = 'create view {} as select id, metadata_id, '.format(view_name)
        sql += ','.join(['{} as "{}"'.format(df, f) for f, df in self.db_fields.items()])
        sql += ' from {} '.format(storage_model._meta.db_table)
        sql += ' where metadata_id = {} '.format(self.pk)
        cur.execute(sql, [])
    

    def form_metadata(self):
        schema = deepcopy(self.schema)
        form_properies = {}
        grid_properties = {}
        for field, property in schema['properties'].items():
            form_properies[field] = {}
            grid_properties[field] = {}
            schema['properties'][field] = {}
            for name, value in property.items():
                if name.startswith('ui:'):
                    form_properies[field][name] = value
                elif name.startswith('grid:'):
                    grid_properties[field][name] = value
                else:
                    schema['properties'][field][name] = value
        form_metadata = {
            'schema': schema,
            'uiSchema': form_properies,
            'grid': grid_properties,
        }
        for root_property in list(form_metadata['schema'].keys()):
            if root_property.startswith('ui:'):
                form_metadata['uiSchema'][root_property] = form_metadata['schema'][root_property]
            elif root_property.startswith('grid:'):
                form_metadata['grid'][root_property] = form_metadata['schema'][root_property]
            if ':' in root_property:
                del form_metadata['schema'][root_property]
        return form_metadata
