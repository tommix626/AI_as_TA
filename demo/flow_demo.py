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
      "content": "The latest Posts are:\n {first_var}"
    },
    {
      "parameter": "first_var",
      "content": "##HTTP_API_Get@0A2w"
    },
    {
      "parameter": "second_var",
      "content": ""
    },
    {
      "parameter": "third_var",
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

input_schemas = r"""
[
    {
        "name": "HTTP_API_Get@5478",
        "description": "A component designed to retrieve information from the Mastodon social network by initiating HTTP GET requests. It fetches the five most recent posts from Mastodon using the specified endpoint and limit parameters.",
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
                "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the Mastodon social network, encompassing data, metadata, or any errors encountered.",
                "type": "json",
                "example": "{ \"posts\": [{ \"id\": 1, \"content\": \"Example post content 1\" }] }"
            }
        ]
    },
    {
        "name": "OpenAIAgent@8321",
        "description": "A specialized language model tailored for analyzing content and themes of received posts. It processes and extracts essential information from the retrieved Mastodon posts.",
        "inputs": [
            {
                "parameter": "input_system_prompt",
                "content": "Analyzing the content and themes of the most recent Mastodon posts to extract key information and trending topics."
            },
            {
                "parameter": "input_user_prompt",
                "content": "##HTTP_API_Get@5478"
            },
            {
                "parameter": "temperature",
                "content": "0.3"
            }
        ]
    },
    {
        "name": "PromptBuilder@8765",
        "description": "A utility designed to construct a morning news report-style summary from the analyzed Mastodon posts. It formats the information for a news reporter presentation.",
        "inputs": [
            {
                "parameter": "template_prompt",
                "content": "Good morning! This is your news reporter with the latest updates. Today's headlines from Mastodon: {first_var}. Now for the detailed news highlights: {second_var}. Concluding with trending topics and sentiments from Mastodon posts."
            },
            {
                "parameter": "first_var",
                "content": "##HTTP_API_Get@5478"
            },
            {
                "parameter": "second_var",
                "content": "##OpenAIAgent@8321"
            },
            {
                "parameter": "third_var",
                "content": ""
            }
        ]
    }
]
"""

# input_schemas = r"""
# [
#     {
#         "name": "HTTP_API_Get_7645",
#         "description": "A component designed to retrieve information from the Mastodon social network by initiating HTTP GET requests. It fetches the five newest posts for analysis in this workflow.",
#         "inputs": [
#             {
#                 "parameter": "url",
#                 "content": "https://mastodon.social/api/v1/timelines/public?limit=5"
#             },
#             {
#                 "parameter": "headers",
#                 "content": ""
#             }
#         ],
#         "outputs": [
#             {
#                 "parameter": "result",
#                 "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from Mastodon, encompassing the data of the five latest posts.",
#                 "type": "json",
#                 "example": "{ \"posts\": [{ \"id\": 1, \"content\": \"Example post content 1\" }, { \"id\": 2, \"content\": \"Example post content 2\" }] }"
#             }
#         ]
#     },
#     {
#         "name": "OpenAIAgent_2276",
#         "description": "A specialized language model tailored for content analysis and extraction. It processes the retrieved posts from HTTP_API_Get_7645 to extract key information, themes, and details.",
#         "inputs": [
#             {
#                 "parameter": "input_system_prompt",
#                 "content": "You are tasked with analyzing the content of the five newest Mastodon posts to extract important details and themes."
#             },
#             {
#                 "parameter": "input_user_prompt",
#                 "content": "##HTTP_API_Get_7645"
#             },
#             {
#                 "parameter": "temperature",
#                 "content": "0.5"
#             }
#         ]
#     },
#     {
#         "name": "PromptBuilder_5402",
#         "description": "A utility designed for structuring summaries in a news report format. It mimics a morning news reporter's style when formatting the extracted post details.",
#         "inputs": [
#             {
#                 "parameter": "template_prompt",
#                 "content": "Good morning! Here are the latest updates from Mastodon: {first_var}. These posts cover various topics including {second_var}. Stay tuned for the detailed summaries."
#             },
#             {
#                 "parameter": "first_var",
#                 "content": "##OpenAIAgent_2276"
#             },
#             {
#                 "parameter": "second_var",
#                 "content": "##OpenAIAgent_2276"
#             },
#             {
#                 "parameter": "third_var",
#                 "content": ""
#             }
#         ],
#         "outputs": [
#             {
#                 "parameter": "parsed_prompt",
#                 "description": "The structured news report format ready for delivery. It encompasses the key details of the five newest Mastodon posts in a format suitable for a morning news broadcast.",
#                 "type": "string",
#                 "example": "Good morning! Here are the latest updates from Mastodon: [Summarized Post 1, Summarized Post 2, Summarized Post 3, Summarized Post 4, Summarized Post 5]. These posts cover various topics including [Theme 1, Theme 2, Theme 3]. Stay tuned for the detailed summaries."
#             }
#         ]
#     }
# ]
# """

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