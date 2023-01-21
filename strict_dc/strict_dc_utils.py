"""
This module is used to help validate the fields
"""

from dataclasses import is_dataclass
from inspect import getmodule
from typing import Any, Dict, Tuple, Union, List, Callable, Type, get_origin, get_args

TYPING_MODULE_NAME: str = 'typing'


def validate_field(given_value: Any, expected_type: Type, *args) -> bool:
    """
    This function receives the `value` of the field, the expected type of the field, and the name of the field.
    It returns `True` if the field is an instance of the expected type, and `False` if not.
    """
    try:
        if is_dataclass(expected_type) and isinstance(given_value, dict):
            given_value = expected_type(**given_value)
        if getmodule(expected_type).__name__ != TYPING_MODULE_NAME:
            return isinstance(given_value, expected_type)
        return _validate_typing_expected_type(given_value, expected_type)
    except Exception:
        return False


def _validate_typing_expected_type(given_value: Any, expected_type: Type) -> bool:
    """
    Validates a field which the expected type of the field is a type from the typing library.
    """
    return FROM_TYPE_TO_VALIDATION_FUNCTION.get(get_origin(expected_type), _default_typing_validation)(given_value,
                                                                                                       expected_type)


def _default_typing_validation(given_value: Any, expected_type: Type):
    if expected_type == Any:
        return True
    return isinstance(given_value, get_origin(expected_type))


def _validate_tuple(given_value: Tuple, expected_type: Type) -> bool:
    tuple_fields: Tuple = get_args(expected_type)
    if not tuple_fields:
        return True
    for i in range(len(given_value)):
        if not validate_field(given_value[i], tuple_fields[i]):
            return False

    return True


def _validate_dict(given_value: Dict, expected_type: Type) -> bool:
    dict_fields: Tuple = get_args(expected_type)
    if not dict_fields:
        return True
    for key, value in given_value.items():
        if not validate_field(key, dict_fields[0]) or not validate_field(value, dict_fields[1]):
            return False

    return True


def _validate_list(given_value: List, expected_type: Type) -> bool:
    list_fields: Tuple = get_args(expected_type)
    if not list_fields:
        return True
    for i in range(len(given_value)):
        if not validate_field(given_value[i], list_fields[0]):
            return False

    return True


def _validate_union(given_value: Union, expected_type: Union) -> bool:
    union_fields: Tuple = get_args(expected_type)
    for field in union_fields:
        if validate_field(given_value, field):
            return True

    return False


FROM_TYPE_TO_VALIDATION_FUNCTION: Dict[Type, Callable[[Any, Type], bool]] = {
    tuple: _validate_tuple,
    dict: _validate_dict,
    list: _validate_list,
    Union: _validate_union
}
