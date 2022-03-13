import json
from copy import deepcopy
from django.apps import apps
from django.db import transaction
from django.db import models
from django.conf import settings
from django.apps import apps
import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'ct_format_class', 'ct_generate_view'
)


class Metadata(models.Model):
    name = models.CharField("Table Name", max_length=64, db_index=True, unique=True)
    title = models.CharField("Title", max_length=128)
    plural = models.CharField("Plural Title", max_length=128)
    storage_app_label = models.CharField("Database Table Name", max_length=64)
    storage_model_name = models.CharField("Database Table Name", max_length=64)
    custom_data = models.JSONField("Schema Data", default=dict)
    custom_to_db_map = models.JSONField("Field Map", default=dict, blank=True)
    db_to_custom_map = models.JSONField("Database Fields", default=dict, blank=True)
    created = models.DateTimeField('Created', auto_now_add=True, db_index=True)
    modified = models.DateTimeField('Modified', auto_now=True)


    class Meta:
        abstract = True
        index_together = (
            ('storage_app_label', 'storage_model')
        )


    def __str__(self):
        return self.name


    @property
    def storage_model(self):
        if not hasattr(self, '_storage_model') or not self._storage_model:
            self._storage_model = apps.get_model(self.storage_app_label, self.storage_model_name)
        return self._storage_model


    @transaction.atomic
    def save(self, *args, **kwargs):
        self._update_field_maps()
        if 'update_fields' in kwargs:
            if 'custom_data' in kwargs['update_fields']:
                # print(kwargs['update_fields'])
                kwargs['update_fields'].append('custom_to_db_map')
                kwargs['update_fields'].append('db_to_custom_map')
        super().save(*args, **kwargs)
        self.create_view()


    def db_field_name(self, type, index):
        return self.storage_model.db_field_name(type, index)


    def _update_field_maps(self):
        ct_storage_fields = self.storage_model._meta.ct_storage_fields
        next_nums = { type_name:0 for type_name in ct_storage_fields.keys() }
        # print(next_nums)
        for field, db_field in self.custom_to_db_map.items():
            type, current_num = self.storage_model.db_field_type(db_field)
            if current_num >= next_nums[type]:
                next_nums[type] = current_num + 1
        # print(next_nums)
        custom_fields = self.get_custom_fields()
        for custom_field in custom_fields:
            type = custom_field['type']
            field_name = custom_field['name']
            if field_name not in self.custom_to_db_map:
                self.custom_to_db_map[field_name] = self.db_field_name(type, next_nums[type])
                next_nums[type] += 1
                self.db_to_custom_map[self.custom_to_db_map[field_name]] = field_name


    def get_custom_fields(self):
        return self._meta.ct_format_class.get_custom_fields(self)


    def get_list_metadata(self):
        return self._meta.ct_format_class.get_list_metadata(self)


    def get_form_metadata(self):
        return self._meta.ct_format_class.get_form_metadata(self)


    def get_django_fields(self):
        django_fields = []
        prefix = self.storage_model._meta.ct_db_field_prefix
        for django_field in self.storage_model._meta.get_fields():
            if django_field.name.startswith(prefix):
                # ignore custom fields
                continue
            # if field.name in field_data:
            #     continue
            if django_field.name == 'metadata':
                # ignore FK to this metadata
                continue
            django_fields.append(django_field)
        return django_fields


    def get_all_field_names(self):
        prefix = self.storage_model._meta.ct_db_field_prefix
        all_field_names = [f['name'] for f in  self.get_custom_fields()]
        all_field_names += [f.name for f in self.get_django_fields()]
        return all_field_names


    def get_db_field_name(self, field_name):
        if field_name in self.custom_to_db_map:
            field_name = self.custom_to_db_map[field_name]
        return field_name


    def create_view(self):
        if not hasattr(self._meta, 'ct_generate_view'):
            return
        if not self._meta.ct_generate_view:
            return
        from django.db import connection
        cur = connection.cursor()
        view_name = '{}_v'.format(self.name)
        sql = 'drop view if exists {}'.format(view_name)
        cur.execute(sql, [])
        sql = 'create view {} as select id, metadata_id, '.format(view_name)
        sql += ','.join(['{} as "{}"'.format(df, f) for f, df in self.custom_to_db_map.items()])
        sql += ' from {} '.format(self.storage_model._meta.db_table)
        sql += ' where metadata_id = {} '.format(self.pk)
        cur.execute(sql, [])
