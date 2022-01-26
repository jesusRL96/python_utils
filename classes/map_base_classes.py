from ..fields import FieldBase, FieldString
from ..functions import nest_dict, flatten_dict

class SingleMapClass:

    def __init__(self) -> None:
        self.errors = []
        self.fields = [y for x in dir(self) if isinstance((y := getattr(self,x)),FieldBase)]
        field_key_names = []
        field_alias = []
        for field in self.fields:
            assert not (field.key_name in field_key_names), f'Field key_name "{field.key_name}" must be unique'
            assert not (field.alias in field_alias), f'Field alias "{field.alias}" must be unique'
            field_key_names.append(field.key_name)
            field_alias.append(field.alias)


    def is_valid(self):
        # iterate over field attributes
        for field in self.fields:
            field.is_valid()
            self.errors = self.errors if field.is_valid() else [*self.errors, {field.alias:field.errors}]
        return not bool(self.errors)


class NestedMapClass(SingleMapClass):

    def __init__(self) -> None:
        super().__init__()  
        self.map_classes = [y for x in dir(self) if isinstance((y := getattr(self,x)),SingleMapClass)]
        self.map_class_errors = []

    def is_valid(self):
        fields_valid = super().is_valid()
        for map_class in self.map_classes:
            self.map_class_errors = self.map_class_errors if map_class.is_valid() else [*self.map_class_errors, map_class.errors]
        return fields_valid and not bool(self.map_class_errors)


#  From dict
class FromDictClass(SingleMapClass):

    def __init__(self, mapping_dict, validation_dict={}) -> None:
        super().__init__()
        self.validation_dict = validation_dict
        print(self.validation_dict)
        flat_dict = flatten_dict(mapping_dict, delimiter='|')
        for flat_index, value in flat_dict.items():
            field = self.create_field(flat_index, value)
            self.fields.append(field)

    def create_field(self, flat_index, value):
        field_validations = self.validation_dict.get(flat_index,{})
        print(flat_index)
        alias = field_validations.get('alias', flat_index)
        return FieldString(flat_index, alias=alias, value=value, value_from_dict=False)

    def serialize_fields(self):
        dict_fields = {x.alias:x.value for x in self.fields}
        nested_dict = nest_dict(dict_fields, '|')
        return nested_dict
