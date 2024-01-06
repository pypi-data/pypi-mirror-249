import pytest
from jsonschematools.core import python_type_to_json_type
from jsonschematools.enums import add_or_update_enum_in_defs, update_property_with_enum


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
        test_schema["properties"]["tags"]["items"] = {"type": "string"}
        with pytest.raises(ValueError) as excinfo:
            update_property_with_enum(test_schema, "IncompatibleEnum", "tags")
        assert "type is incompatible with enum" in str(excinfo.value)

    def test_update_root_property_with_enum(self, test_schema):
        """Test updating a root level property with an enum."""
        schema = update_property_with_enum(test_schema, "StringEnum", "tags")
        assert schema["properties"]["tags"]["items"]["$ref"] == "#/$defs/StringEnum"

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
            update_property_with_enum(test_schema, "NonExistentEnum", "tags")
        assert "Enum 'NonExistentEnum' not found in $defs." in str(excinfo.value)

    def test_property_not_found_error(self, test_schema):
        """Test error when the property is not found."""
        with pytest.raises(ValueError) as excinfo:
            update_property_with_enum(test_schema, "ContactInfo", "nonexistentProperty")
        assert "Property 'nonexistentProperty' not found." in str(excinfo.value)

    def test_property_not_array_type_error(self, test_schema):
        """Test error when the property is not of 'array' type."""
        with pytest.raises(ValueError) as excinfo:
            update_property_with_enum(test_schema, "ContactInfo", "name")
        assert "Property 'name' is not an array." in str(excinfo.value)


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
