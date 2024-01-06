import pytest
from src.jsonschematools.core import python_type_to_json_type
from src.jsonschematools.enums import (
    _update_property, add_or_update_enum_in_defs,
    update_property_with_enum,
)


@pytest.fixture
def test_schema():
    """Provides a basic schema for testing."""
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "$defs": {
            "ContactInfo": {
                "type": "object",
                "properties": {
                    "emails": {"type": "array", "items": {"type": "string"}},
                    "phoneNumbers": {"type": "array", "items": {"type": "string"}},
                },
            },
            "StringEnum": {"type": "string", "enum": ["Option1", "Option2", "Option3"]},
        },
    }


class TestUpdatePropertyWithEnum:
    def test_incompatible_enum_type_error(self, test_schema):
        """Test error when the property and enum types are incompatible."""
        test_schema["$defs"]["IncompatibleEnum"] = {"type": "number", "enum": [1, 2, 3]}
        test_schema["properties"]["name"] = {"type": "string"}
        with pytest.raises(ValueError) as excinfo:
            update_property_with_enum(test_schema, "IncompatibleEnum", "name")
        assert "type is incompatible with enum" in str(excinfo.value)

    def test_update_root_property_with_enum(self, test_schema):
        """Test updating a root level property with an enum."""
        schema = update_property_with_enum(test_schema, "StringEnum", "name")
        assert schema["properties"]["name"]["$ref"] == "#/$defs/StringEnum"

    def test_update_def_property_with_enum(self, test_schema):
        """Test updating a property within $defs with an enum."""
        schema = update_property_with_enum(
                test_schema, "StringEnum", "emails", "ContactInfo"
        )
        assert (
                schema["$defs"]["ContactInfo"]["properties"]["emails"]["items"]["$ref"]
                == "#/$defs/StringEnum"
        )
    def test_enum_not_found_error(self, test_schema):
        """Test error when the enum is not found."""
        with pytest.raises(ValueError) as excinfo:
            update_property_with_enum(test_schema, "NonExistentEnum", "name")
        assert "Enum 'NonExistentEnum' not found in $defs." in str(excinfo.value)

    def test_property_not_found_error(self, test_schema):
        """Test error when the property is not found."""
        with pytest.raises(ValueError) as excinfo:
            update_property_with_enum(test_schema, "ContactInfo", "nonexistentProperty")
        assert "Property 'nonexistentProperty' not found." in str(excinfo.value)

    def test_update_array_property_with_enum(self, test_schema):
        """Test updating an array property with an enum."""
        schema = update_property_with_enum(test_schema, "StringEnum", "tags")
        assert schema["properties"]["tags"]["items"]["$ref"] == "#/$defs/StringEnum"

    def test_update_array_property_with_incompatible_enum_in_defs(self, test_schema):
        """Test updating an array property within $defs with an incompatible enum."""
        # Add a new enum of type 'number' to the schema
        test_schema = add_or_update_enum_in_defs(test_schema, "NumberEnum", [1, 2, 3])
        # Try to update the 'emails' property (which is an array of strings) with the 'NumberEnum'
        with pytest.raises(ValueError) as excinfo:
            schema = update_property_with_enum(
                    test_schema, "NumberEnum", "emails", "ContactInfo"
            )
        assert "Property 'emails' items type is incompatible with enum 'NumberEnum' type." in str(
            excinfo.value)

class TestAddOrUpdateEnumInDefs:
    def test_add_new_enum(self, test_schema):
        """Test adding a new enum to $defs."""
        schema = add_or_update_enum_in_defs(test_schema, "NewEnum", ["A", "B", "C"])
        assert "NewEnum" in schema["$defs"]
        assert schema["$defs"]["NewEnum"] == {"type": "string", "enum": ["A", "B", "C"]}

    def test_update_existing_enum(self, test_schema):
        """Test updating an existing enum in $defs."""
        test_schema["$defs"]["ExistingEnum"] = {"type": "string", "enum": ["X", "Y"]}
        schema = add_or_update_enum_in_defs(
            test_schema, "ExistingEnum", ["A", "B", "C"]
        )
        assert schema["$defs"]["ExistingEnum"] == {
            "type": "string",
            "enum": ["A", "B", "C"],
        }

    def test_empty_enum_values_error(self, test_schema):
        """Test error when enum_values is an empty list."""
        with pytest.raises(ValueError) as excinfo:
            add_or_update_enum_in_defs(test_schema, "EmptyEnum", [])
        assert "enum_values must not be empty." in str(excinfo.value)

    def test_mixed_type_enum_values_error(self, test_schema):
        """Test error when enum_values contain mixed types."""
        with pytest.raises(ValueError) as excinfo:
            add_or_update_enum_in_defs(test_schema, "MixedEnum", [1, "A", True])
        assert "All enum values must be of the same type." in str(excinfo.value)

    def test_no_defs_section_initialization(self, test_schema):
        """Test that a $defs section is initialized if it does not exist."""
        del test_schema["$defs"]
        schema = add_or_update_enum_in_defs(test_schema, "NewEnum", ["A", "B", "C"])
        assert "$defs" in schema
        assert "NewEnum" in schema["$defs"]


class TestPythonTypeToJsonType:
    def test_int_conversion(self):
        """Test conversion of int to 'number'."""
        assert python_type_to_json_type(int) == "number"

    def test_float_conversion(self):
        """Test conversion of float to 'number'."""
        assert python_type_to_json_type(float) == "number"

    def test_str_conversion(self):
        """Test conversion of str to 'string'."""
        assert python_type_to_json_type(str) == "string"

    def test_bool_conversion(self):
        """Test conversion of bool to 'boolean'."""
        assert python_type_to_json_type(bool) == "boolean"

    def test_none_conversion(self):
        """Test conversion of None to 'null'."""
        assert python_type_to_json_type(None) == "null"

    def test_unsupported_type(self):
        """Test handling of unsupported types."""
        with pytest.raises(ValueError) as excinfo:
            python_type_to_json_type(list)
        assert "Unsupported Python type" in str(excinfo.value)


class TestUpdateProperty:
    def test_update_property_with_enum_reference(self):
        """Test updating a property with an enum reference."""
        # Define a schema with a property and an enum
        schema = {
            "properties": {
                "color": {"type": "string"}
            },
            "$defs": {
                "Colors": {"type": "string", "enum": ["Red", "Blue", "Green"]}
            }
        }
        # Update the 'color' property to reference the 'Colors' enum
        _update_property(schema, "color", "Colors", "string")
        # Check that the 'color' property now references the 'Colors' enum
        assert schema["properties"]["color"]["$ref"] == "#/$defs/Colors"

    def test_update_property_with_incompatible_enum_reference(self):
        """Test updating a property with an enum reference of incompatible type"""
        schema = {
            "properties": {
                "color": {"type": "string"}
            },
            "$defs": {
                "Colors": {"type": "number", "enum": [1, 2, 3]}
            }
        }
        # Try to update the 'color' property with the 'Colors' enum
        with pytest.raises(ValueError) as excinfo:
            _update_property(schema, "color", "Colors", "number")
        assert "Property 'color' type is incompatible with enum 'Colors' type." in str(excinfo.value)


    def test_update_property_invalid_prop_name(self):
        """Test attempts to update not existing property."""
        # Define a schema with a property and an enum
        schema = {
            "properties": {
                "color": {"type": "string"}
            },
            "$defs": {
                "Colors": {"type": "string", "enum": ["Red", "Blue", "Green"]}
            }
        }
        # Try to update a non-existent property
        with pytest.raises(ValueError) as excinfo:
            _update_property(schema, "nonexistentProperty", "Colors", "string")
        assert "Property 'nonexistentProperty' not found." in str(excinfo.value)


    def test_update_array_property_with_enum_reference(self):
        """Test updating an array property with an enum reference."""
        # Define a schema with an array property and an enum
        schema = {
            "properties": {
                "colors": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "$defs": {
                "Colors": {"type": "string", "enum": ["Red", "Blue", "Green"]}
            }
        }
        # Update the 'colors' property to reference the 'Colors' enum
        _update_property(schema, "colors", "Colors", "string")
        # Check that the 'colors' property now references the 'Colors' enum
        assert schema["properties"]["colors"]["items"]["$ref"] == "#/$defs/Colors"

    def test_update_array_property_with_incompatible_enum_reference(self):
        """Test updating an array property with an enum reference of incompatible
        type"""
        schema = {
            "properties": {
                "colors": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "$defs": {
                "Colors": {"type": "number", "enum": [1, 2, 3]}
            }
        }
        # Try to update the 'colors' property with the 'Colors' enum
        with pytest.raises(ValueError) as excinfo:
            _update_property(schema, "colors", "Colors", "number")
        assert "Property 'colors' items type is incompatible with enum 'Colors' type." in str(excinfo.value)
