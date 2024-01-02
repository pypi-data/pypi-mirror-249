"""An ultra-lightweight package for validating single conditions.

:Example:
    >>> import onecondition as oc
    >>> oc.validate.not_negative(42)
    >>> oc.validate.range_non_inclusive(0, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must be between 0 and 1 (non-inclusive)
"""

__version__ = "1.1.15"

__all__ = ["ValidationError", "validate", "test"]

# TODO: is_in(value: Any, sequence: Sequence[Any])

from typing import Any


class ValidationError(ValueError):
    """A subclass of ValueError, this is raised any time a validation check fails.

    :param Any value: The value to use in the error message
    :param str condition: The descriptive condition under which the error is raised
    :param str message_format: The format string to use for the message.
        Supports "{value}, {value_repr}, and {condition}"

    :Example:
        >>> raise ValidationError(42, "be the answer to life, the universe, and everything")
        Traceback (most recent call last):
            ...
        onecondition.ValidationError: Value `42` must be the answer to life, the universe, and everything
    """
    def __init__(
            self,
            value: Any,
            condition: str,
            message_format: str = "Value `{value_repr}` must {condition}"
    ):
        message = message_format.format(
            value=value,
            value_repr=repr(value),
            condition=condition)
        super().__init__(message)
