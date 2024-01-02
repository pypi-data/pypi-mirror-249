"""Contains methods to test various conditions about 1 or more values."""
from types import UnionType
from typing import Any, Sequence


def true(value: Any) -> bool:
    """Test if a value is pythonically True.

    :param Any value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> true(True)
        True
        >>> true(False)
        False
        >>> true(None)
        False
        >>> true(0)
        False
        >>> true(1)
        True
        >>> true("")
        False
        >>> true("foobar")
        True
    """
    if value:
        return True

    return False


def false(value: Any) -> bool:
    """Test if a value is pythonically False.

    :param Any value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> false(True)
        False
        >>> false(False)
        True
        >>> false(0)
        True
        >>> false(1)
        False
        >>> false("")
        True
        >>> false("foobar")
        False
    """
    if value:
        return False

    return True


def none(value: Any) -> bool:
    """Test if a value is None.

    :param Any value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> none(None)
        True
        >>> none("")
        False
        >>> none(42)
        False
    """
    return value is None


def specific_type(value: Any, value_type: type | UnionType | tuple[type | UnionType | tuple[Any, ...], ...]) -> bool:
    """Test if a value is a specific type (do not consider inheritance).

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> class TestError(ValueError):
        ...     def __init__(self, message):
        ...         super().__init__(message)
        >>> test_error = TestError("Test")

        >>> specific_type(test_error, TestError)
        True
        >>> specific_type(test_error, ValueError)
        False
        >>> specific_type(test_error, (int, float))
        False
    """
    return type(value) is value_type


def instance(value: Any, value_type: type | UnionType | tuple[type | UnionType | tuple[Any, ...], ...]) -> bool:
    """Test if a value is an instance (the same as or a subclass) of a specific type.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> class TestError(ValueError):
        ...     def __init__(self, message):
        ...         super().__init__(message)
        >>> test_error = TestError("Test")

        >>> instance(test_error, TestError)
        True
        >>> instance(test_error, ValueError)
        True
        >>> instance(test_error, (int, float))
        False
    """
    return isinstance(value, value_type)


def zero(value: int | float) -> bool:
    """Test if a value is exactly equal to 0.

    :param int | float value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> zero(42)
        False
        >>> zero(0)
        True
        >>> zero(-123.45)
        False
    """
    return value == 0


def positive(value: int | float) -> bool:
    """Test if a value is positive (non-zero).

    :param int | float value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> positive(42)
        True
        >>> positive(0)
        False
        >>> positive(-123.45)
        False
    """
    return value > 0


def negative(value: int | float) -> bool:
    """Test if a value is negative (non-zero).

    :param int | float value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> negative(42)
        False
        >>> negative(0)
        False
        >>> negative(-123.45)
        True
    """
    return value < 0


def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> bool:
    """Test if a value is within a specified range (inclusive).

    :param int | float value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> range_inclusive(-123.45, 0, 1)
        False
        >>> range_inclusive(0, 0, 1)
        True
        >>> range_inclusive(0.5, 0, 1)
        True
        >>> range_inclusive(1, 0, 1)
        True
        >>> range_inclusive(42, 0, 1)
        False
    """
    return minimum <= value <= maximum


def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> bool:
    """Test if a value is within a specified range (non-inclusive).

    :param int | float value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> range_non_inclusive(-123.45, 0, 1)
        False
        >>> range_non_inclusive(0, 0, 1)
        False
        >>> range_non_inclusive(0.5, 0, 1)
        True
        >>> range_non_inclusive(1, 0, 1)
        False
        >>> range_non_inclusive(42, 0, 1)
        False
    """
    return minimum < value < maximum


def eq(first: Any, second: Any) -> bool:
    """Test if a value is exactly equal to a second value.

    :param Any first: The value to test.
    :param Any second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> eq(-123.45, 0)
        False
        >>> eq(0, 0)
        True
        >>> eq(42, 0)
        False
        >>> eq("foo", "bar")
        False
        >>> eq("foo", "foo")
        True
    """
    return first == second


def gt(first: int | float, second: int | float) -> bool:
    """Test if a value is greater than a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> gt(-123.45, 0)
        False
        >>> gt(0, 0)
        False
        >>> gt(42, 0)
        True
    """
    return first > second


def lt(first: int | float, second: int | float) -> bool:
    """Test if a value is less than a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> lt(-123.45, 0)
        True
        >>> lt(0, 0)
        False
        >>> lt(42, 0)
        False
    """
    return first < second


def gte(first: int | float, second: int | float) -> bool:
    """Test if a value is greater than or equal to a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> gte(-123.45, 0)
        False
        >>> gte(0, 0)
        True
        >>> gte(42, 0)
        True
    """
    return first >= second


def lte(first: int | float, second: int | float) -> bool:
    """Test if a value is less than or equal to a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool

    :Example:
        >>> lte(-123.45, 0)
        True
        >>> lte(0, 0)
        True
        >>> lte(42, 0)
        False
    """
    return first <= second
