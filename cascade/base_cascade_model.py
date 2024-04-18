import json
import openai


class CascadeModel:
    """
    A base class for a cascade of LLM models designed for langchain orchestration.
    This class provides foundational attributes and methods that specialized models
    (Thinker, Builder, and Constructor) can extend and customize for specific tasks
    in processing and generating structured outputs.

    Attributes:
    - model_name: The name of the specific LLM model to be used.
    - api_key: API key for accessing OpenAI services.
    - instructions: Instruction or prompt template for the model.
    - session: A session object for making API requests. This can be customized or
               extended by subclasses to maintain session state or headers.
    """

    def __init__(self, model_name, openai_api_key=None,**vars):
        """
        Initializes the CascadeModel with the model name, API key, and optional instructions.

        Parameters:
        - model_name (str): Name of the LLM model.
        - api_key (str): OpenAI API key for authentication.
        - instructions (str, optional): Instructions or prompt template for the model.
        """
        self.model_name = model_name
        self.api_key = openai_api_key
        self.instructions = None
        self.session = None  # Placeholder for a session object if needed
        self.model_temperature = 0.7

    def call_model(self, messages):
        """
        Sends the prompt to the specified chat model and retrieves the output.

        Parameters:
        - prompt (str): The prompt to send to the model.

        Returns:
        - output (str): The last response from the assistant.
        """
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=self.model_temperature
        )

        last_message = response['choices'][0]['message']['content'] if response['choices'][0]['message'] else ""
        return last_message

    def execute(self, goal, **kwargs):
        """
        The main execution method that should prepare the prompt, calls the model, and
        processes the output.
        :param **kwargs: some additional flags for each specific model
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def add_few_shot_examples(self,messages):
        for example in self.few_shot_examples:
            messages.append({"role": "user", "content": example['user']})
            messages.append({"role": "assistant", "content": example['assistant']})
        return messages
