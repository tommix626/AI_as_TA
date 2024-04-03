import json

from cascade.cascade_model import CascadeModel
from cascade.define import builder_system_instruction, builder_few_shot_examples
from components.define import component_map

from env import global_api_keys_and_config

class BuilderModel(CascadeModel):
    def __init__(self, model_name):
        super().__init__(model_name, **global_api_keys_and_config)
        self.component_map = component_map
        self.instructions = builder_system_instruction
        self.few_shot_examples = builder_few_shot_examples

    def prepare_prompt(self, goal, thinker_output):
        messages = []

        prompt = self.instructions + "\n\n"
        # TODO: add a structured builder description from the class static variable instead of harding coding it.
        # for component_name, component_cls in self.component_map.items():
        #     prompt += f"**{component_name}**\n{component_cls.builder_description}\n\n"

        messages.append({"role": "system", "content": prompt})
        # Add few-shot examples to the message history
        messages = self.add_few_shot_examples(messages)

        messages.append({"role": "user", "content": goal + thinker_output})

        return messages

    def execute(self, goal, thinker_output):
        """
        Processes the output from the thinker model and prepares it for the constructor model.

        Parameters:
        - thinker_output (str): The output from the thinker model.

        Returns:
        - output_text (str): The processed output ready for the constructor model.
        """
        prompt = self.prepare_prompt(goal,thinker_output)
        output_text = self.call_model(prompt)
        return output_text

if __name__ == '__main__':
    c = BuilderModel("builder")
    thinker_output = "%This is the output from the thinker model%"
    d = c.prepare_prompt(thinker_output)
    print(d)
