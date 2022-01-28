from .validators import (
    ValidatorBase,
    ValidateChoices,
    ValidatorRegExp,
    ValidateIsClose
)


class QueryValidators:

    validators = [ValidateChoices, ValidateIsClose, ValidatorRegExp,]

    def get_validator_types(self):
        return [x.__name__ for x in self.validators]