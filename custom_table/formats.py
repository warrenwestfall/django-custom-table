def snake_to_camel(snake_word):
    camel_word = ''.join(s.capitalize() or '_' for s in snake_word.split('_'))
    return camel_word[0].lower() + camel_word[1:]


class BaseFormat():

    def get_custom_fields(self, metadata):
        """ Must return a list of dictionaries containing field_name and field_type
            [
                {
                    "name": "example_field_name",
                    "type": "char"
                },
            ]
            Overide this in order to store the metadata in the custom_data field
            in a different format than what is expected by Metadata.save().
            This is used by the metadata model to calculate storage mappings
        """
        return metadata.custom_data


    def get_list_metadata(self, metadata):
        """ Should return the metadata required for a Django or front end view to render a grid or list
            Overide this to produce output required by your appication
            If it is desired that the list view be entirely dynamic that method should combine both
            statis Django fields and custom fields
        """
        return self.get_all_fields(metadata)


    def get_form_metadata(self, metadata):
        """ Should return the metadata required for a Django or front end view to render a form
            Overide this to produce output required by your appication
            If it is desired that the form view be entirely dynamic that method should combine both
            statis Django fields and custom fields
        """
        return self.get_all_fields(metadata)
        

    def get_all_fields(self, metadata):
        return self.get_custom_fields(metadata) + self.get_django_fields(metadata)


    def get_django_fields(self, metadata):
        fields = []
        for django_field in metadata.get_django_fields():
            field = {
                'name': django_field.name,
                'type': 'unknown',
                'list': {},
                'form': {},
            }
            field_class = django_field.__class__.__name__
            if field_class.endswith('Field'):
                field['type'] = field_class[:-5].lower()
            if field['type'] == 'bigauto':
                field['type'] = 'integer'
                # field['list']['readonly'] = True
                field['list']['hidden'] = True
                field['form']['readonly'] = True
                field['form']['hidden'] = True
            if django_field.max_length:
                field['form']['max_length'] = django_field.max_length
            fields.append(field)
        return fields


class DefaultFormat(BaseFormat):
    pass


class RestSpaFormat(BaseFormat):
    """ Format metadata for use in a Single Page App with a REST back end
        and a Javascript front end
        Form metadate follows react-jsonschema-form
    """

    def get_list_metadata(self, metadata):
        all_fields = self.get_all_fields(metadata)
        # print(all_fields)
        list_metadata = []
        for field in all_fields:
            type = field['type']
            if type.startswith('indexed_'):
                type = type[8:]
            list_field = {
                'name': field['name'],
                'type': type,
            }
            if 'list' in field:
                for list_property, value in field['list'].items():
                    list_field[list_property] = value
            list_metadata.append(list_field)
        return list_metadata


    def get_form_metadata(self, metadata):
        all_fields = self.get_all_fields(metadata)
        form_metadata = {
            'title': metadata.title,
            'type': 'object',
            'properties': {},
        }
        for field in all_fields:
            properties = {
                'type': field['type'],
            }
            if field['type'] in ('indexed_char', 'char', 'text',):
                properties['type'] = 'string'
            if field['type'] in ('indexed_integer', 'integer',):
                properties['type'] = 'integer'
            if field['type'] == 'float':
                properties['type'] = 'number'
            if field['type'] == 'datetime':
                properties['type'] = 'string'
                properties['format'] = 'date-time'
            if field['type'].startswith('decimal'):
                # _, max_digits, decimal_places = field['type'].split('_')
                properties['type'] = 'string'
                properties['format'] = field['type']
            if 'form' in field:
                for form_property, value in field['form'].items():
                    properties[snake_to_camel(form_property)] = value
            form_metadata['properties'][field['name']] = properties
        return form_metadata
