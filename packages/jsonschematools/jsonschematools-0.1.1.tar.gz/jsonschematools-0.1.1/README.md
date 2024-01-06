# jsonschematools

## Description
`jsonschematools` is a Python library that provides utilities for working with JSON Schema. It includes features for adding and updating enums in the `$defs` section of a JSON schema, and updating a property of a JSON schema with an existing enum reference.

## Installation
To install `jsonschematools`, you can use pip:

```bash
pip install jsonschematools
```

## Usage
Here is a basic example of how to use `jsonschematools`:

```python
from jsonschematools.enums import add_or_update_enum_in_defs, update_property_with_enum

# Define a basic schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "$defs": {},
}

# Add a new enum to the schema
schema = add_or_update_enum_in_defs(schema, "Colors", ["Red", "Blue", "Green"])

# schema now looks like this:
# {
#   "type": "object",
#   "properties": {
#     "name": {
#       "type": "string"
#     },
#     "tags": {
#       "type": "array",
#       "items": {
#         "type": "string"
#       }
#     }
#   },
#   "$defs": {
#     "Colors": {
#       "type": "string",
#       "enum": [
#         "Red",
#         "Blue",
#         "Green"
#       ]
#     }
#   }
# }

# Update a property with the new enum
schema = update_property_with_enum(schema, "Colors", "tags")

# schema now looks like this:
# {
#   "type": "object",
#   "properties": {
#     "name": {
#       "type": "string"
#     },
#     "tags": {
#       "type": "array",
#       "items": {
#         "$ref": "#/$defs/Colors"
#       }
#     }
#   },
#   "$defs": {
#     "Colors": {
#       "type": "string",
#       "enum": [
#         "Red",
#         "Blue",
#         "Green"
#       ]
#     }
#   }
# }
```

## Testing
Tests are written using pytest. To run the tests, use the following command:

```bash
pytest
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
`jsonschematools` is licensed under the MIT License.

## Contact
For any questions or concerns, please open an issue on GitHub.
