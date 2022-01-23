from dataclasses import dataclass
from .field_base import FieldBase

@dataclass
class FieldString(FieldBase):
    value: str = None  

    def value_parse(self):
        self.value = str(self.value)


@dataclass
class FieldInt(FieldBase):
    value: int = None  

    def value_parse(self):
        self.value = int(self.value)