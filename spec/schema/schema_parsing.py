# Example JSON string (representing the LLM chain generated schema)
from schema.utils import convert_json_to_dict
from schema._validate import parse_llm_generated_schema

generated_schema_string = r"""
[
    {
        "name": "HTTP_API_Get_0A2w",
        "inputs": [
            {
                "parameter": "url",
                "content": "https://example.com/api/data"
            },
            {
                "parameter": "header (Optional)",
                "content": "{\"Authorization\": \"Bearer YOUR_API_TOKEN\"}"
            }
        ],
        "outputs": [
            {
                "parameter": "result",
                "content": "{\"data\": [{\"id\": 1, \"name\": \"Example Data\"}]}"
            }
        ]
    }
]

"""

# Conversion and parsing
generated_schema_dict = convert_json_to_dict(generated_schema_string)
print("proceeding to parsing...")
if generated_schema_dict is not None:
    parsed_components = parse_llm_generated_schema(generated_schema_dict)
    for component in parsed_components:
        print(f"Component: {component['name']}")
        print(f"Inputs: {component['inputs']}")
        print(f"Outputs: {component['outputs']}")
else:
    print("Failed to convert JSON string to dictionary.")
