from components.base_component import BaseComponent

class PromptBuilderComponent(BaseComponent):
    builder_description = r"""
    {
"name": "PromptBuilder@{id}",
"description": "A utility designed to dynamically construct prompts by inserting specified string variables into a template. This enables the generation of customized prompts based on user input or contextual data, ideal for crafting specific questions or instructions for chatbots.",
"inputs": [
{
"description": "A template string containing placeholders for variables. These placeholders are identified by braces (e.g., {first_var}) and correspond to the variables provided as additional inputs. The template defines the structure of the final prompt.",
"type": "string",
"example": "user says {first_var}, can you respond in a {second_var} fashion?"
},
{
"description": "The first variable to substitute into the template prompt. This should match the placeholder within the template string.",
"type": "string",
"example": "hello how are you"
},
{
"description": "The second variable for substitution into the template. It fills a designated placeholder within the template to further customize the prompt.",
"type": "string",
"example": "friendly"
},
{
"description": "An optional third variable that can be used for substitution. If the template includes a placeholder for this variable, it will be replaced accordingly. If not used, ensure the template does not include a placeholder for it.",
"type": "string",
"example": "adding additional context if needed"
}
],
"outputs": [
{
"description": "The fully constructed prompt, with all placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to chatbots for processing.",
"type": "string",
"example": "user says hello how are you, can you respond in a friendly fashion?"
}
]
}
"""
    thinker_description = r"""
    {
  "name": "PromptBuilder",
  "description": "A utility designed to dynamically construct prompts by inserting specified string variables into a template. This enables the generation of customized prompts based on user input or contextual data, ideal for crafting specific questions or instructions for chatbots.",
  "inputs": [
    {
      "description": "A template string containing placeholders for variables. These placeholders are identified by braces (e.g., {first_var}) and correspond to the variables provided as additional inputs. The template defines the structure of the final prompt.",
      "type": "string",
      "example": "user says {first_var}, can you respond in a {second_var} fashion?"
    },
    {
      "description": "The first variable to substitute into the template prompt. This should match the placeholder within the template string.",
      "type": "string",
      "example": "hello how are you"
    },
    {
      "description": "The second variable for substitution into the template. It fills a designated placeholder within the template to further customize the prompt.",
      "type": "string",
      "example": "friendly"
    },
    {
      "description": "An optional third variable that can be used for substitution. If the template includes a placeholder for this variable, it will be replaced accordingly. If not used, ensure the template does not include a placeholder for it.",
      "type": "string",
      "example": "adding additional context if needed"
    }
  ],
  "outputs": [
    {
      "description": "The fully constructed prompt, with all placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to chatbots for processing.",
      "type": "string",
      "example": "user says hello how are you, can you respond in a friendly fashion?"
    }
  ]
}
"""
    component_schema = r"""
    {
  "name": "PromptBuilder",
  "description": "A utility designed to dynamically construct prompts by inserting specified string variables into a template. This enables the generation of customized prompts based on user input or contextual data, ideal for crafting specific questions or instructions for chatbots. The variables should always be three variables named first_var, second_var, and third_var. There are no other variables, only those three is available (DO NOT USE fourth_var). You may assign meaning to those variables as you like. If you don't use all of them, leave them as empty string.",
  "inputs": [
    {
      "parameter": "template_prompt",
      "description": "A template string containing placeholders for variables. These placeholders are identified by braces (e.g., {first_var}) and correspond to the variables provided as additional inputs. The template defines the structure of the final prompt.",
      "type": "string",
      "example": "user says {first_var}, can you respond in a {second_var} fashion?"
    },
    {
      "parameter": "first_var",
      "description": "The first variable to substitute into the template prompt. This should match the placeholder within the template string.",
      "type": "string",
      "example": "hello how are you"
    },
    {
      "parameter": "second_var",
      "description": "The second variable for substitution into the template. It fills a designated placeholder within the template to further customize the prompt.",
      "type": "string",
      "example": "friendly"
    },
    {
      "parameter": "third_var",
      "description": "An optional third variable that can be used for substitution. If the template includes a placeholder for this variable, it will be replaced accordingly. If not used, ensure the template does not include a placeholder for it.",
      "type": "string",
      "example": "adding additional context if needed"
    }
  ],
  "outputs": [
    {
      "parameter": "parsed_prompt",
      "description": "The fully constructed prompt, with all placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to chatbots for processing.",
      "type": "string",
      "example": "user says hello how are you, can you respond in a friendly fashion?"
    }
  ]
}

"""
    def __init__(self, component_id, template_prompt=None, first_var=None,second_var=None,third_var=None, **vars):
        super().__init__(component_id)
        self.template_prompt = template_prompt
        self.first_var = first_var
        self.second_var = second_var
        self.third_var = third_var

    @property
    def vars(self):
        return { "first_var":self.first_var,"second_var":self.second_var,"third_var":self.third_var}

    def prepare_inputs(self):
        inputs = {"template_prompt": self.template_prompt() if callable(self.template_prompt) else self.template_prompt}
        for var, value in self.vars.items():
            resolved_value = value() if callable(value) else value
            if not isinstance(resolved_value, str):
                raise TypeError(f"{var} should be a string.")
            inputs[var] = resolved_value

        if not isinstance(inputs['template_prompt'], str):
            raise TypeError("Template prompt should be a string.")

        return inputs

    def execute(self, inputs):
        try:
            template = inputs.pop('template_prompt')
            parsed_prompt = template.format(**inputs)
            self.output = parsed_prompt
            self.logger.info("Prompt built successfully.")
        except Exception as e:
            self.output = {"error": str(e)}
            self.logger.error(f"Failed to build prompt: {e}")
            raise RuntimeError
