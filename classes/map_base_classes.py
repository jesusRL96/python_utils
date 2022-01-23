from ..fields import FieldBase

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