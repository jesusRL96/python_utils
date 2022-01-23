from .map_base_class import SingleMapClass

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