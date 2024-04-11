import json

from schema._parse import _convert_json_to_dict, _parse_cascade_raw_schema
from schema._validate import validate_schema
from jsonschema.exceptions import ValidationError

from schema.define import llm_output_validation_schema


def validate_and_parse_cascade_output(cascade_output_string, validation_schema=llm_output_validation_schema):
    """
    Validates the LLM output against a given schema and parses it if validation passes.
    From this point, everything will be in python.

    :param cascade_output_string: JSON string representation of the LLM output.
    :param validation_schema: JSON schema for validation.
    :return: Parsed components dictionary if validation and parsing are successful, None otherwise.
    """

    # Convert JSON string to Python dictionary
    cascade_output = _convert_json_to_dict(cascade_output_string)

    try:

        # Validate the LLM output
        validate_schema(cascade_output, validation_schema)
        print("LLM output validation passed.")

        # Parse the validated LLM output
        components = _parse_cascade_raw_schema(cascade_output)
        return components

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e.msg}")
    except ValidationError as e:
        print(f"LLM output validation error: {e.message}")

    # Return None if either conversion, validation or parsing fails
    return None

def save_schema_to_file(raw_constructor_output, file_path):
    cascade_output = _convert_json_to_dict(raw_constructor_output)
    with open(file_path, "w") as outfile:
        json.dump(cascade_output, outfile)
def load_schema_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)