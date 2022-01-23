from ctypes import py_object
from dataclasses import InitVar, dataclass, field
from typing import Any, List, Dict


@dataclass
class FieldBase:
    name: str
    alias: str = None
    value: Any = None
    validators: List = field(default_factory=list, repr=False)
    required: bool = True
    value_from_dict: bool = True
    mapping_dict: Dict = field(default_factory=dict, repr=False)
    errors: List = field(init=False, repr=False, default_factory=list)

    def __post_init__(self):
        self.alias = self.alias if bool(self.alias) else self.name

    def value_parse(self):
        self.value = self.value

    def validate_datatype(self):
        data_type = self.__dataclass_fields__['value'].type
        assert isinstance(self.value, data_type), 'Data type does not match'
    
    def is_valid(self):
        if self.value_from_dict:
            assert self.mapping_dict and isinstance(self.mapping_dict,dict), 'Dictionary is required to validate data'
            value_in_dict = self.name in self.mapping_dict.keys()
            self.set_error(not value_in_dict, f'the field {self.alias} is not in the dictionary')
            self.value = self.mapping_dict.get(self.name)
        
        val_required = self.required and not bool(self.value)
        self.set_error(val_required, f'the field {self.alias} is required')

        if self.value:
            self.value_parse()
            self.validate_datatype()
            for validator in self.validators:
                error, error_msg = validator.validate(self.value)
                self.set_error(error, error_msg)
        return not bool(self.errors)
    
    def set_error(self, error, error_msg):
        self.errors = self.errors if not error else list(set([*self.errors, error_msg]))


