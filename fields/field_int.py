from dataclasses import dataclass, field
from .field_base import FieldBase
from typing import cast

@dataclass
class FieldInt(FieldBase):
    value: int = None  

    def value_parse(self):
        self.value = int(self.value)