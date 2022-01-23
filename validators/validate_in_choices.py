from .validator_base import ValidatorBase

class ValidateChoices(ValidatorBase):

    def __init__(self, choices, raise_error=False, error_msg=None) -> None:
        assert isinstance(choices, list), 'Choices must be a list'
        self.choices = choices
        error_msg = f'the value is not in {", ".join(self.choices)}' if not error_msg else error_msg
        super().__init__(error_msg, raise_error)

    def run_validation(self, value):
        return not value in self.choices
    