import requests
from components.base_component import BaseComponent

class HTTPGetComponent(BaseComponent):
    def __init__(self, component_id, url=None, headers=None):
        super().__init__(component_id)
        # URL and headers can be direct values or references to upstream components' outputs
        self.url = url
        self.headers = headers

    def prepare_inputs(self):
        """Prepare the inputs for the HTTP GET request."""
        inputs = {}

        # Resolving 'url'
        if isinstance(self.url, str):
            inputs['url'] = self.url
        elif callable(self.url):
            inputs['url'] = self.url()  # Assuming 'url' is set to a callback function
        else:
            self.logger.error("Invalid Url Meta Type. It should be either a string or a call-back get_output function")
            raise TypeError

        # Resolving 'headers'
        if isinstance(self.headers, dict):
            inputs['headers'] = self.headers
        elif callable(self.headers):
            inputs['headers'] = self.headers()  # Assuming 'headers' is set to a callback function
        else:
            self.logger.error("Invalid headers Meta Type. It should be either a string or a call-back get_output function")
            raise TypeError

        return inputs

    def execute(self, inputs):
        """Execute the HTTP GET request with prepared inputs."""
        try:
            response = requests.get(inputs['url'], headers=inputs.get('headers', {}))
            self.output = response.json()
            self.logger.info(f"HTTP GET request to {inputs['url']} executed successfully.")
        except Exception as e:
            self.logger.error(f"Failed to execute HTTP GET request: {e}")
            self.output = None

        self.is_output_fresh = True if self.output else False

    def get_output(self):
        """Retrieve the component's output if it is fresh."""
        if not self.is_output_fresh:
            self.logger.warning("Attempted to access stale output. Triggering run.")
            self.run()
        return self.output
