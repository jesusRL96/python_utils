from .validator_base import ValidatorBase

class ValidateIsClose(ValidatorBase):

    def __init__(self, close_to, raise_error=False, tol=0, error_msg=None) -> None:
        self.close_to = close_to
        self.tol = tol
        error_msg = f'the value is not close to {close_to}' if not error_msg else error_msg
        super().__init__(error_msg, raise_error)

    def run_validation(self, value):
        import math
        return not math.isclose(value, self.close_to, abs_tol=self.tol)