# Example JSON string (representing the LLM chain generated schema)
from schema.utils import convert_json_to_dict
from schema._validate import parse_llm_generated_schema


# test_schema_parsing.py
import pytest
from schema.utils import convert_json_to_dict
from schema._validate import parse_llm_generated_schema

def test_convert_and_parse_llm_generated_schema():
    generated_schema_string = r"""
    [
    {
      "name": "HTTP_API_Get_0A2w",
      "description": "A component designed to retrieve information from third-party websites by initiating HTTP GET requests. It enables sending requests to specified URLs and optionally includes headers for authentication or specifying request metadata. Tailored for scenarios requiring data extraction from external sources.",
      "inputs": [
        {
          "parameter": "url",
          "content": "##CourseloreGetUnreadNumber"
        },
        {
          "parameter": "header (Optional)",
          "content": ""
        }
      ],
      "outputs": [
        {
          "parameter": "result",
          "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the requested URL, encompassing data, metadata, or any errors encountered during the request. It's crucial for implementing logic based on the response.",
          "type": "json",
          "example": "{\"unread_posts\": 5}"
        }
      ]
    },
    {
      "name": "PromptBuilder_00io",
      "description": "A utility designed to dynamically construct prompts by inserting specified string variables into a template. This enables the generation of customized prompts based on user input or contextual data, ideal for crafting specific questions or instructions for chatbots.",
      "inputs": [
        {
          "parameter": "template_prompt",
          "content": "There are {var1} unread posts on Courselore. Would you like to read them now?"
        },
        {
          "parameter": "var1",
          "content": "##HTTP_API_Get_0A2w"
        }
      ],
      "outputs": [
        {
          "parameter": "parsed_prompt",
          "description": "The fully constructed prompt, with all placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to chatbots for processing.",
          "type": "string",
          "example": "There are 5 unread posts on Courselore. Would you like to read them now?"
        }
      ]
    },
    {
      "name": "HTTP_API_Post_u78y",
      "description": "A component designed to initiate actions on third-party websites by sending HTTP POST requests. This tool sends data to specified URLs, using headers for authentication or specifying request metadata, and a body containing the data to be submitted. It's tailored for scenarios that involve creating, updating, or submitting data to external sources.",
      "inputs": [
        {
          "parameter": "url",
          "content": "https://piazza.com/api/posts/create"
        },
        {
          "parameter": "header",
          "content": "{\"Content-Type\": \"application/json\", \"Authorization\": \"Bearer YOUR_API_TOKEN\"}"
        },
        {
          "parameter": "body",
          "content": "##OpenAIAgent_3W5t"
        }
      ],
      "outputs": [
        {
          "parameter": "result",
          "description": "The response data from the server after processing the POST request, typically in JSON format. This includes any data returned as a result of the action performed, such as a confirmation of creation, details of the updated resource, or error messages.",
          "type": "json",
          "example": "{\"success\": true, \"id\": 123, \"message\": \"Resource created successfully.\"}"
        }
      ]
    }
    ]
    """

    # Conversion and parsing
    generated_schema_dict = convert_json_to_dict(generated_schema_string)
    assert generated_schema_dict is not None, "Conversion from JSON string to dictionary failed."

    parsed_components = parse_llm_generated_schema(generated_schema_dict)
    assert parsed_components is not None, "Parsing of the LLM generated schema failed."
    assert len(parsed_components) == 3, "Expected 3 components to be parsed."
    # Further assertions can be made based on expected contents of the parsed_components
