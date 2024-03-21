import pytest

from schema._validate import validate_and_parse_cascade_output
from schema.define import *

# Sample validation schema as defined previously or import it if it's defined elsewhere

# Test cases

def test_successful_validation_and_parsing():
    # Assuming `validate_and_parse_cascade_output` and `validation_schema` are accessible here
    llm_output_string = """
    [
        {
            "name": "SampleComponent",
            "inputs": [
                {
                    "parameter": "sampleInput",
                    "content": "test input content"
                }
            ],
            "outputs": [
                {
                    "parameter": "sampleOutput",
                    "content": "test output content"
                }
            ]
        }
    ]
    """
    result = validate_and_parse_cascade_output(llm_output_string, llm_output_validation_schema)
    assert result is not None
    assert len(result) == 1
    assert result[0]["name"] == "SampleComponent"
    assert result[0]["inputs"]["sampleInput"] == "test input content"
    assert result[0]["outputs"]["sampleOutput"] == "test output content"

def test_failure_invalid_json_format():
    llm_output_string = """
    { "invalid": "json" }  # Intentionally malformed for this test case
    """
    result = validate_and_parse_cascade_output(llm_output_string, llm_output_validation_schema)
    assert result is None

def test_failure_validation_error():
    # This string misses required 'content' field in inputs and outputs
    llm_output_string = """
    [
        {
            "name": "ComponentWithoutContent",
            "inputs": [
                {
                    "parameter": "missingContent"
                }
            ],
            "outputs": [
                {
                    "parameter": "missingContent"
                }
            ]
        }
    ]
    """
    result = validate_and_parse_cascade_output(llm_output_string, llm_output_validation_schema)
    assert result is None

# Additional tests can be defined here to cover more scenarios



def test_missing_name_field():
    # Schema string with a missing "name" field in one of the components
    schema_string_missing_name = r"""
    [
        {
            "inputs": [
                {"parameter": "url", "content": "https://example.com"}
            ],
            "outputs": [
                {"parameter": "result", "content": "{}"}
            ]
        }
    ]
    """
    result = validate_and_parse_cascade_output(schema_string_missing_name, llm_output_validation_schema)
    assert result is None, "Expected failure when 'name' field is missing."

def test_incorrect_structure():
    # Schema string with an incorrect structure (components not wrapped in a list)
    schema_string_incorrect_structure = r"""
    {
        "name": "IncorrectStructure",
        "inputs": [{"parameter": "url", "content": "https://example.com"}],
        "outputs": [{"parameter": "result", "content": "{}"}]
    }
    """
    result = validate_and_parse_cascade_output(schema_string_incorrect_structure, llm_output_validation_schema)
    assert result is None, "Expected failure with incorrect schema structure."

def test_invalid_content_type():
    # Schema string with invalid content type for "content" (expected string, got object)
    schema_string_invalid_content_type = r"""
    [
        {
            "name": "InvalidContentType",
            "inputs": [
                {"parameter": "url", "content": {"unexpected": "object"}}
            ],
            "outputs": [
                {"parameter": "result", "content": "valid"}
            ]
        }
    ]
    """
    result = validate_and_parse_cascade_output(schema_string_invalid_content_type, llm_output_validation_schema)
    assert result is None, "Expected failure when 'content' field has invalid type."
