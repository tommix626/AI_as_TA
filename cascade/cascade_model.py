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


    def call_model(self, prompt):
        """
        Sends the prompt to the specified LLM model and retrieves the output.

        Parameters:
        - prompt (str): The prompt to send to the model.

        Returns:
        - output (dict): The model's output, parsed from JSON.
        """
        openai.api_key = self.api_key
        response = openai.Completion.create(
            engine=self.model_name,
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024
        )
        return json.loads(response)

    def execute(self, additional_info):
        """
        The main execution method that should prepares the prompt, calls the model, and
        processes the output.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
