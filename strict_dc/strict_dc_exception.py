"""
This exception is used to raise when there is a validation error using the strict dc.
"""

from typing import List, Tuple


class StrictDcError(TypeError):
    def __init__(self, invalid_types: List[Tuple]):
        self.invalid_types = invalid_types
        self.message = self._create_exception_message()
        super().__init__(self.message)

    def _create_exception_message(self) -> str:
        message = ''
        for invalid_type in self.invalid_types:
            message += f'{invalid_type[2]} was expected to be: "{str(invalid_type[1])}", '\
                       f'instead got "{str(invalid_type[0])}"\n'
        return message
