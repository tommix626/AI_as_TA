import requests

from components.base_component import BaseComponent

import requests

import requests
import json
from components.base_component import BaseComponent

class HTTPPostComponent(BaseComponent):
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
