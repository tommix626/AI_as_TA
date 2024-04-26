import openai
from components.base_component import BaseComponent

class OpenAIAgentComponent(BaseComponent):
    thinker_description = r"""
    {
  "name": "OpenAIAgent",
  "description": " A smart agent that is able follow instructions and finish simple task. Underneath, A suite of tools leveraging OpenAI models for tasks ranging from text generation, language translation, to complex question answering. It's designed to interact with OpenAI's API, providing a flexible interface for implementing advanced language model functionalities.",
  "inputs": [
    {
      "description": "A JSON object detailing the task type, parameters, and input text for processing. This specifies the intended use of the OpenAI model, such as generating text, translating languages, or answering questions.",
      "type": "json",
      "example": "{\"task\": \"text-generation\", \"prompt\": \"Write a short story about a robot.\", \"parameters\": {\"max_tokens\": 500}}"
    }
  ],
  "outputs": [
    {
      "description": "The output from the OpenAI model based on the specified task and inputs. It includes the generated text, translation, or answer, along with any other relevant data provided by the model.",
      "type": "json",
      "example": "{\"generated_text\": \"Once upon a time, in a world not unlike our own...\"}"
    }
  ]
}
"""
    builder_description = r"""
    {
  "name": "OpenAIAgent@{id}",
  "description": "A suite of tools leveraging OpenAI models for tasks ranging from text generation, language translation, to complex question answering. It's designed to interact with OpenAI's API, providing a flexible interface for implementing advanced language model functionalities.",
  "inputs": [
    {
      "description": "A JSON object detailing the task type, parameters, and input text for processing. This specifies the intended use of the OpenAI model, such as generating text, translating languages, or answering questions.",
      "type": "json",
      "example": "{\"task\": \"text-generation\", \"prompt\": \"Write a short story about a robot.\", \"parameters\": {\"max_tokens\": 500}}"
    }
  ],
  "outputs": [
    {
      "description": "The output from the OpenAI model based on the specified task and inputs. It includes the generated text, translation, or answer, along with any other relevant data provided by the model.",
      "type": "json",
      "example": "{\"generated_text\": \"Once upon a time, in a world not unlike our own...\"}"
    }
  ]
}"""
    component_schema = r"""
    {
"name": "OpenAIAgent",
"description": "A specialized language model tailored for executing specific tasks by processing structured inputs. This agent interprets and acts upon user-defined prompts and data inputs using adjustable creativity settings.",
"inputs": [
{
"parameter": "input_system_prompt",
"description": "A detailed description of the task or instructions that the model is expected to follow. This should clearly outline the expected output format and the nature of the task, guiding the model towards the desired response.",

"type": "string",

"example": "Please draft a response to a student’s question on the piazza site as an instructor. Be detailed in your response. Embrace a positive and encouraging tone.",

"content": ""
},
{
"parameter": "input_user_prompt",
"description": "User-provided data or queries that the model processes in accordance with the defined system instructions. This can include questions, statements, or raw data needing interpretation or action. This should be the primary place to direct input into this agent. So it likely should only contain ##upstream_component",

"type": "string",

"example":"##GET_API_{some_id}",
"content": ""
},
{
"parameter": "temperature",
"description": "Controls the model's creativity and randomness level, represented as a numerical value between 0 and 1. A lower value (e.g., 0.2) is recommended for tasks requiring high precision and low creativity, such as calculations. A higher value (e.g., 0.7) is suited for tasks that benefit from a more creative approach, such as generating written content or ideation.",

"type": "number",
"example": 0.65,
"content": ""
}
]
}
    """

    def __init__(self, component_id, input_system_prompt=None, input_user_prompt=None, temperature=None, openai_api_key=None, **vars):
        super().__init__(component_id)
        self.api_key = openai_api_key
        self.input_system_prompt = input_system_prompt
        self.input_user_prompt = input_user_prompt
        self.temperature = temperature

    def prepare_inputs(self, user_params=None):

        # Check if temperature is a float; convert to string
        if not callable(self.temperature):
            self.temperature = str(self.temperature) if not isinstance(self.temperature, str) else self.temperature
        return super().prepare_inputs(user_params)

    def execute(self, inputs, user_params=None):
        openai.api_key = self.api_key
        try:
            # Assuming temperature is a float; convert from string
            temperature = float(inputs['temperature'])
            messages = []
            if inputs['input_system_prompt']:  # Check if system prompt is not empty
                messages.append({"role": "system", "content": inputs['input_system_prompt']})
            messages.append({"role": "user", "content": inputs['input_user_prompt']})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature
            )
            self.output = response.choices[0].message['content'].strip()
            self.logger.info("OpenAI chat executed successfully.")
        except Exception as e:
            self.output = {"error": str(e)}
            self.logger.error(f"Failed to execute OpenAI chat: {e}")
            raise RuntimeError