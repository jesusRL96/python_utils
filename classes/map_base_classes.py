from ..fields import *
from ..validators import QueryValidators
from ..functions import nest_dict, flatten_dict, unflatten_dictionary

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

    def __init__(self, mapping_dict, validation_dict={}, validate_full_node = False):
        super().__init__()
        self.validation_dict = validation_dict
        self.validate_full_node = validate_full_node
        self.VALIDATOR_TYPES = QueryValidators().get_validator_types()
        self.FIELD_TYPES = QueryFields().get_field_types()
        flat_dict = flatten_dict(mapping_dict, delimiter='|')
        for flat_index, value in flat_dict.items():
            field = self.create_field(flat_index, value)
            if field:
                self.fields.append(field)

    def create_field(self, flat_index, value):
        field_validations = self.validation_dict.get(flat_index,{})
        # print(flat_index)
        field = None
        if bool(field_validations) or self.validate_full_node:
            type = field_validations.get("type", "FieldString")
            field_validators = field_validations.get("validators",[])
            kwargs_field = {k:v for k,v in field_validations.items() if k not in ['type', 'validators', 'fields']}
            if type not in self.FIELD_TYPES:
                self.errors.append(f'El tipo de campo {type} no es esta registrado')
                return None
            validators = []
            for validator in field_validators:
                validator_name = validator["name"]
                validator_kwargs = validator.get("params")
                if validator_name not in self.VALIDATOR_TYPES:
                    self.errors.append(f'El validador {validator_name} no esta registrado')
                else:
                    try:
                        validator_eval = eval(f'{validator_name}')(**validator_kwargs)
                        validators.append(validator_eval)
                    except Exception as e:
                        self.errors.append(str(e))
            dict_index = flat_index.split("|")
            key_name = dict_index[-1]
            dict_index = dict_index[:-1] if len(dict_index) > 1 else []
            dict_index = field_validations.get('dict_index', "|".join(dict_index))
            kwargs = {
                **kwargs_field,
                "validators": validators,
                "value_from_dict": False,
                "value": value,
                "key_name":key_name,
                "dict_index": dict_index
            }
            field = eval(f'{type}')(**kwargs)
        return field

    def serialize_fields(self, nodo=""):
        nodo = f'{nodo}|' if bool(nodo) else ''
        dict_fields = {f"{nodo}{str(x.dict_index)+'|' if bool(x.dict_index) else ''}{x.alias}":x.value for x in self.fields}
        nested_dict = unflatten_dictionary(dict_fields, '|')
        return nested_dict