import json

import requests
from components.base_component import BaseComponent


def convert_header_str_to_dict(headers_str):
    """
    Converts a string representation of a dictionary (headers) into a dictionary object.
    Handles empty strings and invalid JSON formats gracefully, returning an empty dictionary in such cases.

    Parameters:
    - headers_str (str): The string representation of the headers dictionary.

    Returns:
    - dict: A dictionary object parsed from the input string. Returns an empty dictionary if input is invalid or empty.
    """
    if not headers_str.strip():
        # If the input is an empty string or only contains whitespace, return an empty dictionary
        return {}

    try:
        # Attempt to parse the string into a dictionary
        headers_dict = json.loads(headers_str)
        # Check if the result is indeed a dictionary
        if isinstance(headers_dict, dict):
            return headers_dict
        else:
            # If the parsed object is not a dictionary, log a warning/error and return an empty dictionary
            print("Parsed object is not a dictionary.")
            return {}
    except json.JSONDecodeError:
        # If there is a JSON decoding error, return an empty dictionary
        print("Failed to parse headers string into dictionary.")
        return {}


class HTTPGetComponent(BaseComponent):
    thinker_description = r"""
        {
      "name": "HTTP_API_Get",
      "description": "A component designed to retrieve information from third-party websites by initiating HTTP GET requests. It enables sending requests to specified URLs and optionally includes headers for authentication or specifying request metadata. Tailored for scenarios requiring data extraction from external sources. Should be used for primary data acquisition tools. There's a lot of endpoints implemented in the refs section, all of which is usable",
      "inputs": [
        {
          "description": "The web address (endpoint) from which information is to be retrieved. This should be a fully qualified URL specifying the protocol (http or https), domain, and path to the resource. Use the defined constant below in defs if you need",
          "defs": [
            {
              "refName": "CourseloreGetPost",
              "description": "Endpoint for retrieving a specific post from Courselore using a post ID and an optional limit parameter. Useful for fetching detailed post information.",
              "value": "https://courselore.com/get?id=rorih4jfgee&limit=-1"
            },
            {
              "refName": "CourseloreGetUnreadPost",
              "description": "Endpoint to get the content of unread posts from Courselore for a specific ID. Useful for notification or update mechanisms.",
              "value": "https://courselore.com/get?id=rorih4jfgee"
            },
            {
              "refName": "MastodonSocialGetPost",
              "description": "Endpoint to retrieve recent public posts from the Mastodon social network with a limit on the number of posts. Ideal for integrating public social feeds.",
              "value": "https://mastodon.social/api/v1/timelines/public?limit=2"
            }
          ],
          "type": "string",
          "example": "https://api.example.com/data"
        },
        {
          "description": "A JSON object containing request headers. These headers can include authentication tokens, content type specifications, or any other metadata required by the API or web service being accessed.",
          "type": "json",
          "example": "{\"Authorization\": \"Bearer YOUR_API_TOKEN\", \"Content-Type\": \"application/json\"}"
        }
      ],
      "outputs": [
        {
          "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the requested URL, encompassing data, metadata, or any errors encountered during the request. It's crucial for implementing logic based on the response.",
          "type": "json",
          "example": "{\"data\": [{\"id\": 1, \"name\": \"Example\"}], \"meta\": {\"count\": 1}}"
        }
      ]
    }
        """

    builder_description = r"""
    {
"name": "HTTP_API_Get@{id}",
"description": "A component designed to retrieve information from third-party websites by initiating HTTP GET requests. It enables sending requests to specified URLs and optionally includes headers for authentication or specifying request metadata. Tailored for scenarios requiring data extraction from external sources.",
"inputs": [
{
"description": "The web address (endpoint) from which information is to be retrieved. This should be a fully qualified URL specifying the protocol (http or https), domain, and path to the resource. Use the defined constant below in defs if you need",

"defs": [
{
"refName": "CourseloreGetPost",
"description": "Endpoint for retrieving a specific post from Courselore using a post ID and an optional limit parameter. Useful for fetching detailed post information.",
"value": "https://courselore.com/get?id=rorih4jfgee&limit=-1"
},
{
"refName": "CourseloreGetUnreadPost",
"description": "Endpoint to get the content of unread posts from Courselore for a specific ID. Useful for notification or update mechanisms.",
"value": "https://courselore.com/get?id=rorih4jfgee"
},
{
"refName": "MastodonSocialGetPost",
"description": "Endpoint to retrieve recent public posts from the Mastodon social network with a limit on the number of posts. Ideal for integrating public social feeds.",
"value": "https://mastodon.social/api/v1/timelines/public?limit=2"
}
]
"type": "string",
"example": "https://api.example.com/data"

content: ""
},
{
"description": "A JSON object containing request headers. These headers can include authentication tokens, content type specifications, or any other metadata required by the API or web service being accessed.",
"type": "json",
"example": "{\"Authorization\": \"Bearer YOUR_API_TOKEN\", \"Content-Type\": \"application/json\"}"

content: ""
},
],
"outputs": [
{
"description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the requested URL, encompassing data, metadata, or any errors encountered during the request. It's crucial for implementing logic based on the response.",
"type": "json",
"example": "{\"data\": [{\"id\": 1, \"name\": \"Example\"}], \"meta\": {\"count\": 1}}"
}
]
}"""

    component_schema = r"""
    {
  "name": "HTTP_API_Get",
  "description": "A component designed to retrieve information from third-party websites by initiating HTTP GET requests. It enables sending requests to specified URLs and optionally includes headers for authentication or specifying request metadata. Tailored for scenarios requiring data extraction from external sources.",
  "inputs": [
    {
      "parameter": "url",
      "description": "The web address (endpoint) from which information is to be retrieved. This should be a fully qualified URL specifying the protocol (http or https), domain, and path to the resource. Use the defined constant if you need",
      "defs": [
        {
          "refName": "CourseloreGetPost",
          "description": "Endpoint for retrieving a specific post from Courselore using a post ID and an optional limit parameter. Useful for fetching detailed post information.",
          "value": "https://courselore.com/get?id=rorih4jfgee&limit=-1"
        },
        {
          "refName": "CourseloreGetUnreadPost",
          "description": "Endpoint to get the content of unread posts from Courselore for a specific ID. Useful for notification or update mechanisms.",
          "value": "https://courselore.com/get?id=rorih4jfgee"
        },
        {
          "refName": "MastodonSocialGetPost",
          "description": "Endpoint to retrieve recent public posts from the Mastodon social network with a limit on the number of posts. Ideal for integrating public social feeds.",
          "value": "https://mastodon.social/api/v1/timelines/public?limit=2"
        }
      ],
      "type": "string",
      "example": "https://api.example.com/data",
      "content": ""
    },
    {
      "parameter": "headers",
      "description": "Optional, A JSON object containing request headers. These headers can include authentication tokens, content type specifications, or any other metadata required by the API or web service being accessed.",
      "type": "json",
      "example": "{\"Authorization\": \"Bearer YOUR_API_TOKEN\", \"Content-Type\": \"application/json\"}",
      "content": ""
    }
  ],
  "outputs": [
    {
      "parameter": "result",
      "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the requested URL, encompassing data, metadata, or any errors encountered during the request. It's crucial for implementing logic based on the response.",
      "type": "json",
      "example": "{\"data\": [{\"id\": 1, \"name\": \"Example\"}], \"meta\": {\"count\": 1}}"
    }
  ]
}

    """
    def __init__(self, component_id, url=None, headers=None,**vars):
        super().__init__(component_id)
        # URL and headers can be direct values or references to upstream components' outputs
        self.url = url
        self.headers = headers

    def prepare_inputs(self, user_params=None):
        """
        Prepare the inputs for the HTTP GET request. This method is responsible for preparing the inputs
        that will be used by the HTTP GET request. It does this by calling the `prepare_inputs` method
        from the parent class and converting the 'headers' input from a string to a dictionary.

        Args:
            user_params (dict, optional): Additional user parameters. Defaults to None.

        Returns:
            dict: A dictionary where the keys are the input parameter names and the values are the
                  corresponding input values.
        """

        inputs = super().prepare_inputs(user_params)

        inputs['headers'] = convert_header_str_to_dict(inputs['headers'])

        return inputs

    def execute(self, inputs, user_params=None):
        """Execute the HTTP GET request with prepared inputs.
        :param user_params:
        """
        try:
            response = requests.get(inputs['url'], headers=inputs.get('headers', {}))
            self.output = response.json()
            self.logger.info(f"HTTP GET request to {inputs['url']} executed successfully.")
        except Exception as e:
            self.logger.error(f"Failed to execute HTTP GET request: {e}")
            self.output = None

        self.is_output_fresh = True if self.output else False
        self.output = str(self.output) #chaneg the output to str
