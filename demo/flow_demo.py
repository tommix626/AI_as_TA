"""
a demo of the flow constructor, fed in a cascade output, it should generate a workable function.
"""
from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry
from schema.utils import validate_and_parse_cascade_output

# schema of a flow that summarize the newest ten post to the user.
input_schemas = r"""
[
{
  "name": "HTTP_API_Get@0A2w",
  "description": "A component designed to retrieve information from third-party websites by initiating HTTP GET requests. It enables sending requests to specified URLs and optionally includes headers for authentication or specifying request metadata. Tailored for scenarios requiring data extraction from external sources.",
  "inputs": [
    {
      "parameter": "url",
      "content": "https://mastodon.social/api/v1/timelines/public?limit=5"
    },
    {
      "parameter": "headers",
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
  "name": "PromptBuilder@00io",
  "description": "A utility designed to dynamically construct prompts by inserting specified string variables into a template. This enables the generation of customized prompts based on user input or contextual data, ideal for crafting specific questions or instructions for chatbots.",
  "inputs": [
    {
      "parameter": "template_prompt",
      "content": "The latest Posts are:\n {var1}"
    },
    {
      "parameter": "var1",
      "content": "##HTTP_API_Get@0A2w"
    },
    {
      "parameter": "var2",
      "content": ""
    },
    {
      "parameter": "var3",
      "content": ""
    }
  ],
  "outputs": [
    {
      "parameter": "parsed_prompt",
      "description": "The fully constructed prompt, with all placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to chatbots for processing.",
      "type": "string",
      "example": "The latest Posts are:\n Hello Mastodon!..."
    }
  ]
},
{
  "name": "OpenAIAgent@wer4",
  "description": "A specialized language model tailored for executing specific tasks by processing structured inputs. This agent interprets and acts upon user-defined prompts and data inputs using adjustable creativity settings.",
  "inputs": [
    {
      "parameter": "input_system_prompt",
      "description": "A detailed description of the task or instructions that the model is expected to follow. This should clearly outline the expected output format and the nature of the task.",
      "content": "Please summarize the following mastodon post in a paragraph, this summary will be played through a TTS service when user eat breakfast, address the user by Tom and greet him as you should in the scenario."
    },
    {
      "parameter": "input_user_prompt",
      "description": "User-provided data or queries that the model processes in accordance with the defined system instructions. This can include questions, statements, or raw data needing interpretation or action.",
      "content": "##PromptBuilder@00io"
    },
    {
      "parameter": "temperature",
      "description": "Controls the model's creativity and randomness level, represented as a numerical value between 0 and 1. A lower value (e.g., 0.2) is recommended for tasks requiring high precision and low creativity, such as calculations. A higher value (e.g., 0.7) is suited for tasks that benefit from a more creative approach, such as generating written content or ideation.",
      "content": "0.7"
    }
  ]
}
]

"""



if __name__ == '__main__':
    print("Parsing schemas...")
    parsed_input_schemas = validate_and_parse_cascade_output(input_schemas)

    print("Setting up factory....")
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)
    factory.setup(parsed_input_schemas)

    print("Running factory....")
    result = factory.run()
    print("Result = \n" + result)