from components.base_component import BaseComponent

class PromptBuilderComponent(BaseComponent):
    def __init__(self, component_id, template_prompt=None, **vars):
        super().__init__(component_id)
        self.template_prompt = template_prompt
        self.vars = vars

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
