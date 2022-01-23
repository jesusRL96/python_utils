

class ValidatorBase:
    def __init__(self, error_msg, raise_error=False) -> None:
        self.raise_error = raise_error
        self.error_msg = error_msg
    
    def run_validation(self, value):
        return True

    def validate(self, value):
        is_valid = self.run_validation(value)
        if is_valid:
            self.error = self.error_msg
            assert not self.raise_error, self.error_msg
        else:
            self.error = ''    
        return is_valid, self.error_msg
