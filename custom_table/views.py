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
    always_update_fields = []


    def get_metadata_queryset(self):
        """
        Return the list of custom tables and their metadata for this view.
        """
        # print(self.metadata_model)
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
            'storage_app_label':  metadata.storage_app_label,
            'storage_model_name': metadata.storage_model_name,
            'custom_data': metadata.custom_data,
        }

    
    @classmethod
    def format_data_for_detail(cls, metadata):
        data = cls.format_data_for_list(metadata)
        data['list_metadata'] = metadata.get_list_metadata()
        data['form_metadata'] = metadata.get_form_metadata()
        return data


    def get_list(self):
        metadata_queryset = self.get_metadata_queryset()
        return [self.format_data_for_list(metadata) for metadata in metadata_queryset]


    def get_metadata_record(self, name_or_pk):
        metadata_queryset = self.get_metadata_queryset()
        try:
            return get_object_or_404(metadata_queryset, pk=int(name_or_pk))
        except ValueError:
            return get_object_or_404(metadata_queryset, name=name_or_pk)


    def get_detail(self, name_or_pk):
        detail_record = self.get_metadata_record(name_or_pk)
        return self.format_data_for_detail(detail_record)


    def create(self, post_data):
        metadata_queryset = self.get_metadata_queryset()
        new_record = metadata_queryset.model()
        for field in metadata_queryset.model._meta.get_fields():
            if field.name in post_data:
                setattr(new_record, field.name, post_data[field.name])
        new_record.save()
        return new_record


    def update_fields(self, name_or_pk, data):
        detail_record = self.get_metadata_record(name_or_pk)
        update_fields = self.always_update_fields
        for field_name, value in data.items():
            setattr(detail_record, field_name, value)
            update_fields.append(field_name)
        detail_record.save(update_fields=update_fields)


    def delete_record(self, name_or_pk):
        detail_record = self.get_metadata_record(name_or_pk)
        detail_record.delete()


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
        for field_name in self.metadata.get_all_field_names():
            columns.append(field_name)
        for detail_record in self.queryset.all():
            record = {}
            for field_name in columns:
                record[field_name] = detail_record.get_custom_value(field_name)
            records.append(record)
        return { 'records': records }


    def get_grid_list(self):
        rows = []
        columns = []
        # if self.include_metadata:
        #     columns = [{'name': 'pk', 'title': 'pk'}]
        # else:
        #     columns = ['pk']
        for field in self.metadata.get_list_metadata():
            # if 'visible' in field and not field['visible']:
            #     continue
            if self.include_metadata:
                column_data = field
            else:
                column_data = field['name']
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
        # print(columns, rows)
        return {'columns': columns, 'rows': rows}


    def get_detail(self, pk):
        detail_record = get_object_or_404(self.queryset, pk=pk)
        data_record = {
            'pk': detail_record.pk
        }
        for field_name in self.metadata.get_all_field_names():
            value = detail_record.get_custom_value(field_name)
            data_record[field_name] = value
        if self.include_metadata:
            form_metadata = self.metadata.get_form_metadata()
            return { 'metadata': form_metadata, 'data': data_record }
        else:
            return data_record


    def create(self, post_data):
        new_record = self.queryset.model(metadata = self.metadata)
        for field_name in self.metadata.get_all_field_names():
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
            self.storage_model = self.metadata.storage_model
            self.queryset = self.storage_model.objects.filter(metadata=self.metadata)
        return super().dispatch(request, *args, **kwargs)
