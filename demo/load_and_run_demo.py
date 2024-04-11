import json

from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry
from schema.utils import load_schema_from_file, validate_and_parse_cascade_output

if __name__ == '__main__':
    print("Loading schema from cascade_output.json...")
    # Adjust the file path as necessary
    input_schemas = load_schema_from_file("../tmp/cascade_output.json")

    print("Parsing schemas...")
    # Ensure your validate_and_parse_cascade_output function can handle the direct JSON object
    parsed_input_schemas = validate_and_parse_cascade_output(json.dumps(input_schemas))

    print("Setting up factory....")
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)
    factory.setup(parsed_input_schemas)

    print("Running factory....")
    result = factory.run()
    print("Result = \n" + result)