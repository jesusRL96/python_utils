from .validator_base import ValidatorBase
import re

class ValidateRegExp(ValidatorBase):

    def __init__(self, reg_exp, raise_error=False, alias_pat=None, error_msg=None) -> None:
        self.reg_exp = reg_exp
        self.alias_pat = alias_pat if alias_pat else self.reg_exp
        error_msg = f'the value does not match with the pattern "{self.alias_pat}"' if not error_msg else error_msg
        super().__init__(error_msg, raise_error)

    def run_validation(self, value):
        reg_patt = re.compile(self.reg_exp)
        match = reg_patt.match(value)
        return not bool(match)



class ValidateChoices(ValidatorBase):

    def __init__(self, choices, raise_error=False, error_msg=None) -> None:
        assert isinstance(choices, list), 'Choices must be a list'
        self.choices = choices
        error_msg = f'the value is not in {", ".join(self.choices)}' if not error_msg else error_msg
        super().__init__(error_msg, raise_error)

    def run_validation(self, value):
        return not value in self.choices



class ValidateIsClose(ValidatorBase):

    def __init__(self, close_to, raise_error=False, tol=0, error_msg=None) -> None:
        self.close_to = close_to
        self.tol = tol
        error_msg = f'the value is not close to {close_to}' if not error_msg else error_msg
        super().__init__(error_msg, raise_error)

    def run_validation(self, value):
        import math
        return not math.isclose(value, self.close_to, abs_tol=self.tol)