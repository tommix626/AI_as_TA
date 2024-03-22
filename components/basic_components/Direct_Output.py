"""
Used for final information output, placeholder TODO
will have the option to display result to a website, an HTTP Get API, etc...
"""


import requests
from components.base_component import BaseComponent

class DirectOutputComponent(BaseComponent):
    component_schema = r"""
    {
"name": "Direct_Output",
"description": "",
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
"refName": "CourseloreGetUnreadNumber",
"description": "Endpoint to get the number of unread posts from Courselore for a specific ID. Useful for notification or update mechanisms.",
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
"parameter": "header (Optional)",
"description": "A JSON object containing request headers. These headers can include authentication tokens, content type specifications, or any other metadata required by the API or web service being accessed.",
"type": "json",
"example": "{\"Authorization\": \"Bearer YOUR_API_TOKEN\", \"Content-Type\": \"application/json\"}"

content: ""
},
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
