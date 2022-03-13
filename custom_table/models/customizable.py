from django.db import models
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'ct_metadata_model', 'ct_db_field_prefix', 'ct_storage_fields',
)


def generate_db_field_name(type, index, ct_db_field_prefix):
    return f'{ct_db_field_prefix}{type}{index:0>4}'


class CustomizableMeta(models.base.ModelBase):

    def __new__(cls, name, bases, attrs):
        # bases = (models.Model, CustomizableMixin)
        if not hasattr(attrs['Meta'], 'ct_db_field_prefix'):
            setattr(attrs['Meta'], 'ct_db_field_prefix', 'ctf_')
        ct_db_field_prefix = getattr(attrs['Meta'], 'ct_db_field_prefix')
        ct_metadata_model = getattr(attrs['Meta'], 'ct_metadata_model')
        ct_storage_fields = getattr(attrs['Meta'], 'ct_storage_fields')
        attrs['metadata'] = models.ForeignKey(ct_metadata_model, on_delete=models.PROTECT, db_index=True)
        for type_name, data_type in ct_storage_fields.items():
            for i in range(data_type['num_to_create']):
                db_field_name = generate_db_field_name(type_name, i, ct_db_field_prefix)
                db_field = data_type['field_class'](null=True,blank=True,**data_type['field_class_params'])
                attrs[db_field_name] = db_field
        return super().__new__(cls, name, bases, attrs)


class CustomizableMixin:
    
    @classmethod
    def db_field_name(cls, type, index):
        return generate_db_field_name(type, index, cls._meta.ct_db_field_prefix)


    @classmethod
    def db_field_type(cls, db_field):
        type = db_field[len(cls._meta.ct_db_field_prefix):-4]
        current_num = int(db_field[-4:])
        return type, current_num


    def get_custom_value(self, field_name):
        field_name = self.metadata.get_db_field_name(field_name)
        return getattr(self, field_name)


    def set_custom_value(self, field_name, value):
        field_name = self.metadata.get_db_field_name(field_name)
        setattr(self, field_name, value)
        return field_name
