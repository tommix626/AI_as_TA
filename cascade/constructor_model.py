import json

from cascade.cascade_model import CascadeModel
from cascade.define import constructor_few_shot_examples, constructor_system_instruction
from components.define import component_map

from env import global_api_keys_and_config
class ConstructorModel(CascadeModel):
    def __init__(self, model_name):
        super().__init__(model_name,**global_api_keys_and_config)
        self.component_map = component_map
        self.instructions = constructor_system_instruction
        self.few_shot_examples = constructor_few_shot_examples

    def prepare_prompt(self, builder_output_context,builder_output_relationships):
        messages = []

        prompt = self.instructions + "\n\n"
        for component_name, component_cls in self.component_map.items():
            prompt += f"**{component_name}**\n{component_cls.component_schema}\n\n"
        # prompt += "\n".join(self.few_shot_examples) + "\n\n"
        prompt += "**Context:**\n" + builder_output_context + "\n\n"
        prompt += "**The relationships are as follows:**\n" + builder_output_relationships + "\n\n"
        prompt += "Now generate the result for other components used in this flow:"

        messages.append({"role": "system", "content": prompt})
        # Add few-shot examples to the message history TODO: factor out as a base method
        for example in self.few_shot_examples:
            messages.append({"role": "assistant", "content": example['assistant']})
            messages.append({"role": "user", "content": example['user']})

        return messages

    def execute(self, builder_output):
        prompt = self.prepare_prompt(builder_output)
        output_text = self.call_model(prompt)
        return output_text

if __name__ == '__main__':
    c = ConstructorModel("tt")
    d = c.prepare_prompt("%This is builder output context%","%This is builder output_relationship%")
    print(d)