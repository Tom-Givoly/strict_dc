"""
This class is used to validate the types of a dataclass.
"""
from typing import List, Tuple

from .strict_dc_exception import StrictDcError
from .strict_dc_utils import validate_field


class StrictDC:
    def __post_init__(self):
        fields: List[Tuple] = list(
            zip(list(self.__dict__.values()), list(self.__annotations__.values()), list(self.__dict__.keys())))
        invalid_types: List[Tuple] = [field for field in fields if not validate_field(*field)]
        if invalid_types:
            raise StrictDcError(invalid_types=invalid_types)
