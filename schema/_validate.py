from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_schema(input_schema, predefined_schema):
    try:
        validate(instance=input_schema, schema=predefined_schema)
        print("Schema validation passed.")
        return True
    except ValidationError as e:
        print(f"Schema validation error: {e.message}")
        return False
