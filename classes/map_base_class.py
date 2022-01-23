from ..fields import FieldBase

class SingleMapField:

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