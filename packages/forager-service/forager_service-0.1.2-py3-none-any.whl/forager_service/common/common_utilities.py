"""Utilities for Forager project."""
from __future__ import annotations

from typing import Any

from forager_service.common.validators import (
    params_validators,
    special_validators,
    validators,
)


def create_and_validate_params(operation_type: str, **kwargs: Any) -> dict:
    """
    Add params from keyword arguments.

    :param operation_type: str Name of request operation.
    :param kwargs: dict Key word arguments for particular operation.
    :return: dict Params for request.
    """
    special_validators.validate_arguments(operation_type, kwargs)
    param_dict: dict = {}
    for key, element in kwargs.items():
        if element is not None:
            for validator in validators[key]:
                validator(key, element)
            param_dict[key] = element
    for validation_handler in params_validators['required_arguments']:
        validation_handler(operation_type, param_dict)
    return param_dict
