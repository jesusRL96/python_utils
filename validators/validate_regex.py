from .validator_base import ValidatorBase
import re

class ValidatorRegExp(ValidatorBase):

    def __init__(self, reg_exp, raise_error=False, alias_pat=None, error_msg=None) -> None:
        self.reg_exp = reg_exp
        self.alias_pat = alias_pat if alias_pat else self.reg_exp
        error_msg = f'the value does not match with the pattern "{self.alias_pat}"' if not error_msg else error_msg
        super().__init__(error_msg, raise_error)

    def run_validation(self, value):
        reg_patt = re.compile(self.reg_exp)    
        match = reg_patt.match(value)
        return not bool(match)
    