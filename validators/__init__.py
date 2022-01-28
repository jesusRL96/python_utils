from .validators import (
    ValidatorBase,
    ValidateChoices,
    ValidateRegExp,
    ValidateIsClose
)


class QueryValidators:

    validators = [ValidateChoices, ValidateIsClose, ValidateRegExp,]

    def get_validator_types(self):
        return [x.__name__ for x in self.validators]