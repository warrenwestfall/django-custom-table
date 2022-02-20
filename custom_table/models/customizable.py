from django.db import models


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
}


def db_field_name(type, index):
    return '{0}{1:0>4}'.format(type, index)


def db_field_type(db_field):
    type = db_field[:-4]
    current_num = int(db_field[4:])
    return type, current_num


class CustomizableMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        # bases = (models.Model, CustomizableMixin)
        metadata_model = getattr(attrs['Meta'], 'metadata_model')
        delattr(attrs['Meta'], 'metadata_model')
        attrs['metadata'] = models.ForeignKey(metadata_model, on_delete=models.PROTECT, db_index=True)
        for type_name, data_type in DATA_TYPES.items():
            for i in range(data_type['num_to_create']):
                attrs[db_field_name(type_name, i)] = data_type['field_class'](null=True,blank=True,**data_type['field_class_params'])
        return super().__new__(cls, name, bases, attrs)


class CustomizableMixin:
    def get_custom_value(self, field_name):
        field_name = self.metadata.get_db_field_name(field_name)
        return getattr(self, field_name)


    def set_custom_value(self, field_name, value):
        field_name = self.metadata.get_db_field_name(field_name)
        setattr(self, field_name, value)
        return field_name
