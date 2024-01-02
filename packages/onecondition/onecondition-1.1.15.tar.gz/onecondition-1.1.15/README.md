# 1️⃣ OneCondition
### An ultra-lightweight package for validating single conditions.
[![Python Version](https://img.shields.io/pypi/pyversions/onecondition?logo=python&logoColor=white)](https://pypi.org/project/onecondition/)
[![PyPI Version](https://img.shields.io/pypi/v/onecondition?logo=PyPI&logoColor=white)](https://pypi.org/project/onecondition/)

[![GitHub Build](https://img.shields.io/github/actions/workflow/status/nimaid/python-onecondition/master.yml?logo=GitHub)](https://github.com/nimaid/python-onecondition/actions/workflows/master.yml)
[![Codecov Coverage](https://img.shields.io/codecov/c/github/nimaid/python-onecondition?logo=codecov&logoColor=white)](https://codecov.io/gh/nimaid/python-onecondition)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6016e7276903495c9d4a6f0dc89d2904)](https://app.codacy.com/gh/nimaid/python-onecondition/dashboard)

[![License](https://img.shields.io/pypi/l/onecondition?logo=opensourceinitiative&logoColor=white)](https://github.com/nimaid/python-onecondition/raw/main/LICENSE)
[![PyPI Downloads](https://img.shields.io/pypi/dm/onecondition.svg?label=pypi%20downloads&logo=PyPI&logoColor=white)](https://pypi.org/project/onecondition/)

## Why?
Often when writing Python code, you will need to validate one or more conditions about a value, and raise an error if those conditions aren't valid.
The most simple example is as follows:
```python
def inverse(value):
    # Validate that the input is a positive number
    if not isinstance(value, (int, float)):
        raise ValueError("Value must be either an int or a float")
    if not value > 0:
        raise ValueError("Value must be positive (non-zero)")
    
    return 1 / value
```
This works for very simple cases, but what if we wanted to format more information into the error messages?
What if we want a custom error type to represent specifically a validation error?
What if we need to do 20, or 200 validations, instead of 2?
You can start to see how quickly your boilerplate for validation could clutter up your code.

`onecondition` aims to solve this issue with a simple design philosophy:

**You should only have to write one line of code in order to validate one condition.**

*(And that line should be less than 100 characters long.)*
## Usage

<!--
```doctest
>>> import onecondition as oc

>>> def inverse(value):
...     oc.validate.instance(value, (int, float))
...     oc.validate.positive(value)
...     return 1 / value

>>> inverse(4)
0.25
>>> inverse(0)
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `0` must be positive (non-zero)
>>> inverse("foobar")
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `'foobar'` must be an instance of (<class 'int'>, <class 'float'>), not a <class 'str'>

```
-->

The most common usage of `onecondition` is to validate that the parameters passed to a function are valid.
The `validate` submodule provides a [large number of functions](https://onecondition.readthedocs.io/en/latest/autoapi/onecondition/validate/index.html#functions) that allow validating many aspects about a value.
```python
import onecondition as oc
import onecondition.validate

def inverse(value):
    # Validate that the input is a positive number
    oc.validate.instance(value, (int, float))
    oc.validate.positive(value)
    
    return 1 / value
```
Now, if you run something like `inverse(4)`, you will get the expected output of `0.25`.

However, running `inverse(0)` would give the following error:
```
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `0` must be positive (non-zero)
```
Similarly, running `inverse("foobar")` would result in the following:
```
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `'foobar'` must be an instance of (<class 'int'>, <class 'float'>), not a <class 'str'>
```
Isn't that much nicer than writing all that code yourself?

# Full Documentation
<p align="center"><a href="https://onecondition.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="onecondition on Read the Docs"></a></p>
