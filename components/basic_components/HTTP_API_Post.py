import requests

from components.base_component import BaseComponent

import requests

import requests
import json
from components.base_component import BaseComponent

class HTTPPostComponent(BaseComponent):
    component_schema = r"""
    {
"name": "HTTP_API_Post",
"description": "A component designed to initiate actions on third-party websites by sending HTTP POST requests. This tool sends data to specified URLs, using headers for authentication or specifying request metadata, and a body containing the data to be submitted. It's tailored for scenarios that involve creating, updating, or submitting data to external sources.",
"inputs": [
{
"parameter": "url",
"description": "The web address (endpoint) to which the data is to be sent. This should be a fully qualified URL specifying the protocol (http or https), domain, and the path to the resource where the POST request will be received.",
"type": "string",
"example": "https://api.example.com/resource/create"

content: ""
},
{
"parameter": "header",
"description": "A JSON object containing the necessary request headers. These headers may include content type declarations, authentication tokens, or any other metadata required by the target API or service to process the request properly.",
"type": "json",
"example": "{\"Content-Type\": \"application/json\", \"Authorization\": \"Bearer YOUR_API_TOKEN\"}",

content: ""
},
{
"parameter": "body",
"description": "The actual data to be sent in the POST request. This JSON object should contain all the necessary information the API needs to create or update resources, or perform the intended action.",
"type": "json",
"example": "{\"name\": \"New Resource\", \"description\": \"Details about the resource.\"}",

content: ""
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
"""
    def __init__(self, component_id, url=None, headers=None, body=None):
        super().__init__(component_id)
        self.url = url
        self.headers = headers
        self.body = body

    def prepare_inputs(self):
        inputs = {}

        # URL
        inputs['url'] = self.url() if callable(self.url) else self.url
        if not isinstance(inputs['url'], str):
            raise TypeError("URL should be a string.")

        # Headers
        inputs['headers'] = self.headers() if callable(self.headers) else self.headers
        if not isinstance(inputs['headers'], str):
            raise TypeError("Headers should be a string.")

        # Body
        inputs['body'] = self.body() if callable(self.body) else self.body
        if not isinstance(inputs['body'], str):
            raise TypeError("Body should be a string.")

        return inputs

    def execute(self, inputs):
        try:
            # Convert 'headers' and 'body' from string to dictionary for the request
            headers = json.loads(inputs['headers'])
            body = json.loads(inputs['body'])
            response = requests.post(inputs['url'], headers=headers, json=body)
            self.output = response.json()
            self.logger.info(f"HTTP POST request to {inputs['url']} executed successfully.")
        except Exception as e:
            self.output = {"error": str(e)}
            self.logger.error(f"Failed to execute HTTP POST request: {e}")
            raise RuntimeError
