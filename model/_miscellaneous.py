import re
import stringcase # Ensure this library is installed: `pip install stringcase`
from typing import Any
from collections.abc import Iterable
  

# Define LIST_LIKE if necessary
LIST_LIKE = (list, tuple, set)

def verify_iterable(value: Any) -> Iterable:
    """
    Returns iterables, except strings, wraps simple types into tuple.
    """
    return value if isinstance(value, LIST_LIKE) else (value,)

def sentencecase_to_snakecase(s: str) -> str:
    """
    Convert sentence case to snake_case.

    Args:
        s: Input string in sentence case

    Returns:
        string in snake_case form
    """
    return stringcase.snakecase(s).lower()

def sentencecase_to_pascalcase(s: str) -> str:
    """
    Convert sentence case to PascalCase.

    Args:
        s: Input string in sentence case

    Returns:
        string in PascalCase form
    """
    return re.sub(r"(?:^| )([a-zA-Z])", lambda match: match.group(1).upper(), s)
