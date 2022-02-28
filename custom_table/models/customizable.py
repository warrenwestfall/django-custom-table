from django.db import models
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'metadata_model', 'db_field_prefix',
)

DATA_TYPES = {
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
    "money": {
        "num_to_create": 30,
        "field_class": models.DecimalField,
        "field_class_params": {
            "max_digits": 1000,
            "decimal_places": 2,
        },
    },
    "decimal": {
        "num_to_create": 10,
        "field_class": models.DecimalField,
        "field_class_params": {
            "max_digits": 1000,
            "decimal_places": 500,
        },
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
}


def generate_db_field_name(type, index, db_field_prefix):
    return '{2}{0}{1:0>4}'.format(type, index, db_field_prefix)


def db_field_type(db_field):
    type = db_field[:-4]
    current_num = int(db_field[4:])
    return type, current_num


class CustomizableMeta(models.base.ModelBase):

    def __new__(cls, name, bases, attrs):
        # bases = (models.Model, CustomizableMixin)
        if not hasattr(attrs['Meta'], 'db_field_prefix'):
            setattr(attrs['Meta'], 'db_field_prefix', 'ctf_')
        db_field_prefix = getattr(attrs['Meta'], 'db_field_prefix')
        metadata_model = getattr(attrs['Meta'], 'metadata_model')
        attrs['metadata'] = models.ForeignKey(metadata_model, on_delete=models.PROTECT, db_index=True)
        for type_name, data_type in DATA_TYPES.items():
            for i in range(data_type['num_to_create']):
                db_field_name = generate_db_field_name(type_name, i, db_field_prefix)
                db_field = data_type['field_class'](null=True,blank=True,**data_type['field_class_params'])
                attrs[db_field_name] = db_field
        return super().__new__(cls, name, bases, attrs)


class CustomizableMixin:
    
    @classmethod
    def db_field_name(cls, type, index):
        return generate_db_field_name(type, index, cls._meta.db_field_prefix)


    def get_custom_value(self, field_name):
        field_name = self.metadata.get_db_field_name(field_name)
        return getattr(self, field_name)


    def set_custom_value(self, field_name, value):
        field_name = self.metadata.get_db_field_name(field_name)
        setattr(self, field_name, value)
        return field_name
