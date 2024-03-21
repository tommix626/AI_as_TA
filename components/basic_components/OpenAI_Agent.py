import openai
from components.base_component import BaseComponent

class OpenAIAgentComponent(BaseComponent):
    component_schema = r"""
    {
"name": "OpenAIAgent",
"description": "A specialized language model tailored for executing specific tasks by processing structured inputs. This agent interprets and acts upon user-defined prompts and data inputs using adjustable creativity settings.",
"inputs": [
{
"parameter": "input_system_prompt",
"description": "A detailed description of the task or instructions that the model is expected to follow. This should clearly outline the expected output format and the nature of the task, guiding the model towards the desired response.",

"type": "string",

"example": "Please draft a response to a student’s question on the piazza site as an instructor. Be detailed in your response. Embrace a positive and encouraging tone.”,

"content": ""
},
{
"parameter": "input_user_prompt",
"description": "User-provided data or queries that the model processes in accordance with the defined system instructions. This can include questions, statements, or raw data needing interpretation or action. This should be the primary place to direct input into this agent. So it likely should only contain ##upstream_component",

"type": "string",

“example”:”##GET_API_{some_id}”
"content": ""
},
{
"parameter": "temperature",
"description": "Controls the model's creativity and randomness level, represented as a numerical value between 0 and 1. A lower value (e.g., 0.2) is recommended for tasks requiring high precision and low creativity, such as calculations. A higher value (e.g., 0.7) is suited for tasks that benefit from a more creative approach, such as generating written content or ideation.",

"type": "number",
"example": 0.65
"content": ""
}
]
}
    """
    def __init__(self, component_id, api_key, input_system_prompt=None, input_user_prompt=None, temperature=None):
        super().__init__(component_id)
        self.api_key = api_key
        self.input_system_prompt = input_system_prompt
        self.input_user_prompt = input_user_prompt
        self.temperature = temperature

    def prepare_inputs(self):
        inputs = {}

        # System Prompt
        inputs['input_system_prompt'] = self.input_system_prompt() if callable(self.input_system_prompt) else self.input_system_prompt
        if not isinstance(inputs['input_system_prompt'], str):
            raise TypeError("System prompt should be a string.")

        # User Prompt
        inputs['input_user_prompt'] = self.input_user_prompt() if callable(self.input_user_prompt) else self.input_user_prompt
        if not isinstance(inputs['input_user_prompt'], str):
            raise TypeError("User prompt should be a string.")

        # Temperature
        inputs['temperature'] = str(self.temperature() if callable(self.temperature) else self.temperature)

        return inputs

    def execute(self, inputs):
        openai.api_key = self.api_key
        try:
            # Assuming temperature is a float; convert from string
            temperature = float(inputs['temperature'])
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=inputs['input_user_prompt'],
                temperature=temperature
            )
            self.output = response.choices[0].text.strip()
            self.logger.info("OpenAI agent executed successfully.")
        except Exception as e:
            self.output = {"error": str(e)}
            self.logger.error(f"Failed to execute OpenAI agent: {e}")
            raise RuntimeError
