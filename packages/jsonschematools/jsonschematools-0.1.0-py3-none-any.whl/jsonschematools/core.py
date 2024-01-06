def python_type_to_json_type(python_type: type[int | float | str | bool | None]):
    """
    Converts a given Python data type to its corresponding JSON schema type.

    The `python_type` provided should be one of: int, float, str, bool, None.

    This function handles the following transformations:
        - `int` or `float` to 'number'
        - `str` to 'string'
        - `bool` to 'boolean'
        - `None` to 'null'

    If an unsupported `python_type` is provided, a `ValueError` is raised.

    Args:
        python_type: The Python data type to be converted to a JSON schema equivalent.

    Returns:
        str: The JSON schema data type corresponding to the given Python data type.

    Raises:
        ValueError: If Python type is not supported. This error is chosen over
            TypeError as the function is intended to map a finite set of Python types to
            JSON  schema types. Any type outside this set, although technically a type
            issue, is treated as an 'invalid value' in the context of this specific
            mapping function.

    Example:
        >>> python_type_to_json_type(int)
        'number'
        >>> python_type_to_json_type(bool)
        'boolean'
        >>> python_type_to_json_type(None)
        'null'
        >>> python_type_to_json_type(list)
        Traceback (most recent call last):
        ...
        ValueError: Unsupported Python type: <class 'list'>
    """
    if python_type in [int, float]:
        return "number"
    elif python_type == str:
        return "string"
    elif python_type == bool:
        return "boolean"
    elif python_type is None:
        return "null"
    else:
        raise ValueError(f"Unsupported Python type: {python_type}")
