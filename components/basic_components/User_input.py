from components.base_component import BaseComponent
import json


class UserInputComponent(BaseComponent):
    # Descriptions based on the earlier specifications
    component_schema = r"""
    {
  "name": "UserInput",
  "description": "Captures user input and makes it available as the starting point of a processing workflow. This component is always used as a top-level upstream component, working as a start of the flow.",
  "inputs": [
    {
      "parameter": "user_input",
      "description": "The data input by the user that will be copied to the output without modification. When using this omponent, place a placeholder text or example to guide the user on the expected input format.",
      "type": "user_param",
      "example": "Enter your query here or specify parameters for data retrieval."
    }
  ],
  "outputs": [
    {
      "parameter": "output",
      "description": "The exact data entered by the user, passed through without modification to ensure accuracy and integrity in subsequent processing.",
      "type": "string",
      "example": "User-entered query or data parameters."
    }
  ]
}
"""
    thinker_description = r"""The UserInputComponent is crucial in systems that initiate processes based on direct user interaction. This component serves as the primary entry point for user data, making it indispensable in applications where the workflow's direction or output is dictated by user preferences, queries, or commands. Its role is to accurately capture and forward user inputs to subsequent processing stages, ensuring that the data provided by the user is preserved without modification. Ideal scenarios for its deployment include interactive query systems, dynamic reporting tools, and personalized service applications where user feedback or commands are necessary to drive the system's logic. By employing this component at the beginning of such workflows, systems can dynamically adapt to varied inputs, providing tailored responses or actions based on individual user needs."""
    builder_description = r"""The UserInputComponent is designed for seamless integration into any workflow that requires an initial user input as a trigger or data source. From a technical standpoint, this component is implemented to accept a wide range of input types — text, numbers, or structured formats — making it highly adaptable to different user interaction paradigms. The simplicity of its design, where it acts merely as a conduit for passing user input into the system, means that it can be easily configured and deployed without the need for extensive setup. Developers can integrate this component at the start of any pipeline that depends on user data, ensuring that the input is immediately available for downstream components without delay. Furthermore, due to its design as a generic input handler, this component can be reused across multiple applications with minimal changes, thereby standardizing how user input is handled in diverse systems.
    Its input parameter, 'user_input', is a placeholder for any data entered by the user. It will be dynamically changed by the system at running phase. so adding the component itself will be sufficient to capture user input. this component should not appears as the downstream of any other components."""

    def __init__(self, component_id, user_input, **kwargs):
        super().__init__(component_id)
        self.user_input = user_input  # Directly using the input provided during initialization, factory pass it in

    def prepare_inputs(self, user_params=None):
        # update the user_input from the user_params if available
        self.user_input = user_params[self.component_id][
            "user_input"] if user_params and self.component_id in user_params else self.user_input

        return super().prepare_inputs(user_params=user_params)

    def execute(self, inputs, user_params=None):
        # Check if user input is provided in the user_params
        self.user_input = user_params[self.component_id][
            "user_input"] if user_params and self.component_id in user_params else self.user_input
        # Directly pass the user input as output
        self.output = self.user_input
        self.is_output_fresh = True
