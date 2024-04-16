import json

from cascade.cascade_model import CascadeModel
from cascade.define import thinker_system_instruction, thinker_few_shot_examples, thinker_system_closing_instruction
from components.define import component_map

from env import global_api_keys_and_config
class ThinkerModel(CascadeModel):
    def __init__(self, model_name):
        super().__init__(model_name,**global_api_keys_and_config)
        self.component_map = component_map
        self.instructions = thinker_system_instruction
        self.few_shot_examples = thinker_few_shot_examples

    def prepare_prompt(self, user_input, user_prompting=None):
        add = thinker_system_closing_instruction
        if(user_prompting != None and user_prompting != ""):
            add = user_prompting

        messages = []

        prompt = self.instructions + "\n\n"
        comp_prompt,name_prompt = "",""
        for component_name, component_cls in self.component_map.items():
            if(component_name.startswith("Test")):
                continue
            comp_prompt += f"**{component_name}**\n{component_cls.thinker_description}\n\n"
            name_prompt += component_name + ", "
        prompt += name_prompt + ".\n" + comp_prompt + thinker_system_closing_instruction

        # TODO: add a structured thinker description from the class static variable instead of harding coding it.
        # for component_name, component_cls in self.component_map.items():
        #     prompt += f"**{component_name}**\n{component_cls.thinker_description}\n\n"

        messages.append({"role": "system", "content": prompt})
        # Add few-shot examples to the message history
        messages = self.add_few_shot_examples(messages)

        messages.append({"role": "user", "content": user_input})

        return messages

    def execute(self, user_input, user_prompting=None):
        prompt = self.prepare_prompt(user_input, user_prompting)
        output_text = self.call_model(prompt)
        return output_text

if __name__ == '__main__':
    c = ThinkerModel("thinker")
    d = c.prepare_prompt("%This is user_input%", "")
    print(d)