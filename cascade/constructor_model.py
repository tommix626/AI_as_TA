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

    def prepare_prompt(self, goal, builder_output, user_prompting, builder_output_context=None,builder_output_relationships=None): #TODO parse the output
        messages = []
        add = self.instructions
        if(user_prompting != ""):
            add = user_prompting
        prompt = add + "\n\n"
        for component_name, component_cls in self.component_map.items():
            prompt += f"**{component_name}**\n{component_cls.component_schema}\n\n"
        # prompt += "\n".join(self.few_shot_examples) + "\n\n"

        prompt += "Now according to the context and relationship, generate the resulting schema for all components used in the flow in a Json Array:"

        messages.append({"role": "system", "content": prompt})
        # Add few-shot examples to the message history
        messages = self.add_few_shot_examples(messages)

        # input_prompt = ""
        # input_prompt += "**Context:**\n" + builder_output_context + "\n\n"
        # input_prompt += "**The relationships are as follows:**\n" + builder_output_relationships + "\n\n"
        input_prompt = builder_output

        messages.append({"role": "user", "content": goal + input_prompt})

        return messages

    def execute(self, goal, builder_output, user_prompting):
        prompt = self.prepare_prompt(goal, builder_output, user_prompting)
        output_text = self.call_model(prompt)
        return output_text


if __name__ == '__main__':
    c = ConstructorModel("tt")
    d = c.prepare_prompt("%This is builder output context%","%This is builder output_relationship%", "")
    print(d)