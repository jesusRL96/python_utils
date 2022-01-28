from .field_base import FieldBase
from .fields import (
    FieldInt,
    FieldString,
    FieldDecimal
)

class QueryFields:
    fields = [FieldInt, FieldString,FieldDecimal]

    def get_field_types(self):
        return [x.__name__ for x in self.fields]