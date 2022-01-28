from dataclasses import dataclass
from decimal import Decimal
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

@dataclass
class FieldDecimal(FieldBase):
    value: Decimal = None  

    def value_parse(self):
        self.value = Decimal(str(self.value))