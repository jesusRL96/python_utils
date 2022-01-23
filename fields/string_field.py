from dataclasses import dataclass, field
from .field_base import FieldBase
from typing import cast

@dataclass
class FieldString(FieldBase):
    value: str = None  

    def value_parse(self):
        self.value = str(self.value)
   