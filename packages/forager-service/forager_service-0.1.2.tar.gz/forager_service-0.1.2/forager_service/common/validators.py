"""Validators for arguments."""
import re
from typing import Callable, Union

from forager_service.common.exceptions import ArgumentValidationError

operation_arguments = {
    'domain-search': {'domain', 'company', 'limit', 'offset', 'type', 'seniority', 'department', 'required_field'},
    'email-finder': {'domain', 'company', 'first_name', 'last_name', 'full_name', 'max_duration'},
    'email-verifier': {'email'},
    'email-count': {'domain', 'company', 'type'},
}


class CommonValidators(object):
    """General type validators."""

    def validate_str(self, key: str, param_value: str) -> None:
        """Validate param_value is str type."""
        if not isinstance(param_value, str):
            raise ArgumentValidationError('{key} has wrong type.'.format(key=key))

    def validate_int(self, key: str, param_value: int) -> None:
        """Validate param_value is int type."""
        if not isinstance(param_value, int):
            raise ArgumentValidationError('{key} has wrong type.'.format(key=key))

    def validate_email(self, key: str, param_value: str) -> None:
        """Validate email."""
        specials = "!#$%&'*+-/=?^_`{|?."
        specials = re.escape(specials)
        regex = re.compile(
            '^(?!['
            + specials
            + '])(?!.*['
            + specials
            + ']{2})(?!.*['
            + specials
            + ']$)[A-Za-z0-9'
            + specials
            + ']+(?<!['
            + specials
            + '])@[A-Za-z0-9.-]+[.][A-Za-z]{2,4}$',
        )
        if not re.fullmatch(regex, param_value):
            raise ArgumentValidationError('{key} has invalid value.'.format(key=key))


common_validators = CommonValidators()


class KwargsValidators(object):
    """Kwargs validators."""

    def validate_email_type(self, key: str, param_value: str) -> None:
        """Validate email type."""
        if param_value not in {'personal', 'generic'}:
            raise ArgumentValidationError('{key} has wrong value.'.format(key=key))

    def validate_seniority(self, key: str, param_value: str) -> None:
        """Validate seniority kwarg."""
        value_list: list = param_value.split(', ')
        for elem in value_list:
            if elem not in {'junior', 'senior', 'executive'}:
                raise ArgumentValidationError('{key} has wrong value.'.format(key=key))

    def validate_department(self, key: str, param_value: str) -> None:
        """Validate department param_value."""
        value_list: list = param_value.split(', ')
        sample_set: set = {
            'executive',
            'it',
            'finance',
            'management',
            'sales',
            'legal',
            'support',
            'hr',
            'marketing',
            'communication',
        }
        for elem in value_list:
            if elem not in sample_set:
                raise ArgumentValidationError('{key} has wrong value.'.format(key=key))

    def validate_required_field(self, key: str, param_value: str) -> None:
        """Validate required field argument."""
        value_list: list = param_value.split(', ')
        for elem in value_list:
            if elem not in {'full_name', 'position', 'phone_number'}:
                raise ArgumentValidationError('{key} has wrong value.'.format(key=key))

    def validate_max_duration(self, key: str, param_value: int) -> None:
        """Validate max duration param_value."""
        high_limit: int = 20
        low_limit: int = 3
        if high_limit < param_value or param_value < low_limit:
            raise ArgumentValidationError('{key} should be in range from 3 to 20.'.format(key=key))


kwargs_validators = KwargsValidators()


class SpecialValidators(object):
    """Special case validators."""

    def validate_arguments(self, operation: str, arguments_dict: dict) -> None:
        """Validate params in allowed list for the operation."""
        arguments_set: set[str] | None = operation_arguments.get(operation)
        if arguments_set is None:
            raise ArgumentValidationError('{op} is not allowed operation'.format(op=operation))
        for key in arguments_dict:
            if key not in arguments_set:
                raise ArgumentValidationError(
                    'Argument {arg} is not from arguments list for {op} operation'.format(arg=key, op=operation),
                )

    def validate_required_arguments(self, key: str, param_dict: dict) -> None:
        """Validate presence required argument in the list."""
        if key in {'domain-search', 'email-finder', 'email-count'}:
            if 'domain' not in param_dict and 'company' not in param_dict:
                raise ArgumentValidationError(
                    'For {key} operation should be defined domain or company'.format(key=key),
                )

    def validate_email_finder_required_argument(self, key: str, param_dict: dict) -> None:
        """Validate precense at least 'full_name' or 'first_name' and 'last_name'."""
        if key == 'email-finder':
            if 'full_name' not in param_dict and ('first_name' not in param_dict or 'last_name' not in param_dict):
                raise ArgumentValidationError(
                    'At least first_name and last_name or full_name should be in param_dict.',
                )


special_validators = SpecialValidators()

Dict_A = dict[str, Union[str, int]]
Callable_A = Callable[[str, Dict_A], None]
Callable_B = Callable[[str, str], None]
Callable_C = Callable[[str, int], None]
Tuple_A = tuple[Callable_B, ...]
Tuple_B = tuple[Callable_C, ...]

validators: dict[str, Union[Tuple_A, Tuple_B]] = {
    'domain': (common_validators.validate_str,),
    'company': (common_validators.validate_str,),
    'limit': (common_validators.validate_int,),
    'offset': (common_validators.validate_int,),
    'type': (common_validators.validate_str, kwargs_validators.validate_email_type),
    'seniority': (common_validators.validate_str, kwargs_validators.validate_seniority),
    'department': (common_validators.validate_str, kwargs_validators.validate_department),
    'required_field': (common_validators.validate_str, kwargs_validators.validate_required_field),
    'first_name': (common_validators.validate_str,),
    'last_name': (common_validators.validate_str,),
    'full_name': (common_validators.validate_str,),
    'max_duration': (common_validators.validate_int, kwargs_validators.validate_max_duration),
    'email': (common_validators.validate_str, common_validators.validate_email),
}


params_validators: dict[str, tuple[Callable_A, Callable_A]] = {
    'required_arguments': (
        special_validators.validate_required_arguments,
        special_validators.validate_email_finder_required_argument,
    ),
}
