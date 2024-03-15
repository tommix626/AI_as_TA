import openai
from components.base_component import BaseComponent

class OpenAIAgentComponent(BaseComponent):
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
