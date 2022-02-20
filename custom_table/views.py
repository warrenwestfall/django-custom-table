import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from custom_table.models import Metadata


class CustomTableMixin():
    metadata_queryset = None
    metadata_model = None


    def get_metadata_queryset(self):
        """
        Return the list of custom tables and their metadata for this view.
        """
        print(self.metadata_model)
        if self.metadata_queryset is not None:
            metadata_queryset = self.metadata_queryset
            if isinstance(metadata_queryset, QuerySet):
                metadata_queryset = metadata_queryset.all()
        elif self.metadata_model is not None:
            metadata_queryset = self.metadata_model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.metadata_model, %(cls)s.metadata_queryset, or override "
                "%(cls)s.get_metadata_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return metadata_queryset


class BaseMetadataView(View, CustomTableMixin):
    
    @staticmethod
    def format_data_for_list(metadata):
        return {
            'name': metadata.name,
            'title': metadata.title,
            'plural': metadata.plural,
            'endpoint': '/rest/{}/'.format(metadata.name)
        }

    
    @classmethod
    def format_data_for_detail(cls, metadata):
        data = cls.format_data_for_list(metadata)
        data.update(metadata.form_metadata())
        return data


    def get_list(self):
        metadata_queryset = self.get_metadata_queryset()
        return [self.format_data_for_list(metadata) for metadata in metadata_queryset]


    def get_detail(self, name):
        metadata_queryset = self.get_metadata_queryset()
        metadata = get_object_or_404(metadata_queryset, name=name)
        return self.format_data_for_detail(metadata)


class BaseCustomTableView(View, CustomTableMixin):
    metadata_queryset = None
    metadata_model = None
    include_metadata = True
    # TODO support get filters
    # TODO pagination


    def get_object_list(self):
        metadata_queryset = self.get_metadata_queryset()
        columns = ['pk']
        records = []
        for field, properties in self.metadata.schema['properties'].items():
            if 'grid:visible' in properties and not properties['grid:visible']:
                continue
            columns.append(field)
        for detail_record in self.queryset.all():
            record = {}
            for field in columns:
                record[field] = detail_record.get_custom_value(field)
            records.append(record)
        return { 'records': records }


    def get_grid_list(self):
        rows = []
        if self.include_metadata:
            columns = [{'name': 'pk', 'title': 'pk'}]
        else:
            columns = ['pk']
        for field, properties in self.metadata.schema['properties'].items():
            if 'grid:visible' in properties and not properties['grid:visible']:
                continue
            if self.include_metadata:
                column_data = properties
                column_data['name'] = field
            else:
                column_data = field
            columns.append(column_data)
        for detail_record in self.queryset.all():
            row = [] # [detail_record.pk]
            for field in columns:
                if self.include_metadata:
                    field_name = field['name']
                else:
                    field_name = field
                row.append(detail_record.get_custom_value(field_name))
            rows.append(row)
        return {'columns': columns, 'rows': rows}


    def get_detail(self, pk):
        detail_record = get_object_or_404(self.queryset, pk=pk)
        data_record = {
            'pk': detail_record.pk
        }
        for field_name, properties in self.metadata.schema['properties'].items():
            value = detail_record.get_custom_value(field_name)
            data_record[field_name] = value
        if self.include_metadata:
            form_metadata = self.metadata.form_metadata()
            return { 'metadata': form_metadata, 'data': data_record }
        else:
            return data_record


    def create(self, post_data):
        db_data = {}
        new_record = self.queryset.model(metadata = self.metadata)
        for field_name, properties in self.metadata.schema['properties'].items():
            if field_name in post_data:
                new_record.set_custom_value(field_name, post_data[field_name])
        new_record.save()
        return new_record


    def update_fields(self, pk, data):
        detail_record = get_object_or_404(self.queryset, pk=pk)
        update_fields = ['modified']
        for field_name, value in data.items():
            db_field_name = detail_record.set_custom_value(field_name, value)
            update_fields.append(db_field_name)
        detail_record.save(update_fields=update_fields)


    def delete_record(self, pk):
        detail_record = get_object_or_404(self.queryset, pk=pk)
        detail_record.delete()


    def dispatch(self, request, name=None, *args, **kwargs):
        metadata_queryset = self.get_metadata_queryset()
        if name:
            self.metadata = get_object_or_404(metadata_queryset, name=name)
            self.storage_model = self.metadata.get_storage_model()
            self.queryset = self.storage_model.objects.filter(metadata=self.metadata)
        return super().dispatch(request, *args, **kwargs)
