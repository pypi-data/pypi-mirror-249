from typing import Optional

from .core import python_type_to_json_type


def add_or_update_enum_in_defs(
    schema: dict[str, any],
    enum_name: str,
    enum_values: list[int | float | str | bool | None],
) -> dict[str, any]:
    """
    Adds a named enumeration to the `$defs` section of a JSON schema.

    Args:
        schema (dict): The JSON schema in which enumeration is to be added.
        enum_name (str): The unique identifier for the enumeration.
        enum_values (list): Enumeration values with a common type.

    Returns:
        dict: The updated JSON schema with the newly added enumeration.

    Raises:
        ValueError: If `enum_values` is an empty list or if the elements of
            `enum_values` are not of the same Python type.

    Notes:
        - If a `$defs` key does not exist in the provided schema, it is initialized.

        - If an enumeration with the same name already exists in `$defs`,
            it is updated with the new `enum_values`.

    Example:
        >>> schema = { "$defs": {} }
        >>> enum_name = "Colors"
        >>> enum_values = ["Red", "Blue", "Green"]
        >>> add_or_update_enum_in_defs(schema, enum_name, enum_values)
        {'$defs': {'Colors': {'type': 'string', 'enum': ['Red', 'Blue', 'Green']}}}
    """
    # Ensure $defs exists in the schema
    if "$defs" not in schema:
        schema["$defs"] = {}

    # Raise an error if enum_values is empty
    if not enum_values:
        raise ValueError("enum_values must not be empty.")

    # Check that all enum values are of the same type
    first_value_type = type(enum_values[0])
    if not all(isinstance(value, first_value_type) for value in enum_values):
        raise ValueError("All enum values must be of the same type.")

    # Determine the type of the enum values
    enum_type = python_type_to_json_type(first_value_type)

    # Create or update the enum in $defs
    schema["$defs"][enum_name] = {"type": enum_type, "enum": enum_values}

    return schema


def _update_property(
    location: dict[str, any],
    prop_name: str,
    enum_name: str,
    enum_type: str
) -> None:
    """
    Updates a property in a specified location to reference an existing enum.

    This is a helper function used by `update_property_with_enum`.

    Args:
        location (dict[str, any]): The location in the schema where the property is.
        prop_name (str): Name of the property to be updated with the enum reference.
        enum_name (str): Name of an existing enum.
        enum_type (str): Type of the enum.

    Raises:
        ValueError: An error is thrown if the property doesn't exist or if the property and enum types are incompatible.
    """
    # Get the property
    prop = location.get("properties", {}).get(prop_name)
    # If the property does not exist, raise an error
    if prop is None:
        raise ValueError(f"Property '{prop_name}' not found.")
    # Get the type of the property
    prop_type = prop.get("type")
    # If the property is an array, get the type of its items
    if "items" in prop:
        prop_type = prop["items"].get("type")
        # If the items type is not the same as the enum type, raise an error
        if prop_type and prop_type != enum_type:
            raise ValueError(
                    f"Property '{prop_name}' items type is incompatible with enum '{enum_name}' type."
            )
        # Update the items of the property to reference the enum
        prop["items"]["$ref"] = f"#/$defs/{enum_name}"
    # If the property type is not the same as the enum type, raise an error
    elif prop_type and prop_type != enum_type:
        raise ValueError(
                f"Property '{prop_name}' type is incompatible with enum '{enum_name}' type."
        )
    # If the property is not an array, update the property to reference the enum
    else:
        prop["$ref"] = f"#/$defs/{enum_name}"

def update_property_with_enum(
    schema: dict[str, any],
    enum_name: str,
    property_name: str,
    def_name: Optional[str] = None,
) -> dict[str, any]:
    """
    Updates a property of a specified JSON schema with an existing enum reference.

    Args:
        schema (dict[str, any]): The input JSON schema intended for modification.
        enum_name (str): Name of an existing enum present under `$defs`.
        property_name (str): Name of the property to be updated with the enum reference.
        def_name (Optional[str], optional): If property lies under a definition in `$defs`, give definition's name. Defaults to None.

    Returns:
        dict[str, any]: The JSON schema modified to include the enum reference to the specified property.

    Raises:
        ValueError: An error is thrown if the property doesn't exist, if the `$defs` or specified enum doesn't exist, or if the property and enum types are incompatible.
    """
    # Check if the enum exists in the schema
    if enum_name not in schema.get("$defs", {}):
        raise ValueError(f"Enum '{enum_name}' not found in $defs.")

    # Get the type of the enum
    enum_type = schema["$defs"][enum_name]["type"]

    # If a definition name is provided, update the property within the definition
    if def_name:
        if def_name in schema["$defs"]:
            _update_property(schema["$defs"][def_name], property_name, enum_name, enum_type)
        else:
            raise ValueError(f"$defs '{def_name}' not found in schema.")
    # If no definition name is provided, update the property at the root level of the schema
    else:
        _update_property(schema, property_name, enum_name, enum_type)

    return schema
