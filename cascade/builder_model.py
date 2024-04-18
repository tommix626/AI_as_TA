import json
import logging
import re
from typing import List, Any

from cascade.base_cascade_model import CascadeModel
from cascade.define import builder_system_instruction, builder_few_shot_examples, builder_system_closing_instruction
from components.define import component_map

from env import global_api_keys_and_config


class BuilderModel(CascadeModel):
    def __init__(self, model_name):
        super().__init__(model_name, **global_api_keys_and_config)
        self.component_map = component_map
        self.instructions = builder_system_instruction
        self.few_shot_examples = builder_few_shot_examples
        self.model_temperature = 0.4

    def prepare_prompt(self, goal, thinker_output, user_prompting=None):
        messages = []
        add = builder_system_closing_instruction
        if (user_prompting != None and user_prompting != ""):
            add = user_prompting

        prompt = self.instructions + "\n\n"
        comp_prompt, name_prompt = "", ""
        for component_name, component_cls in self.component_map.items():
            if (component_name.startswith("Test")):
                continue
            comp_prompt += f"**{component_name}**\n{component_cls.thinker_description}\n\n"
            name_prompt += component_name + ", "
        prompt += name_prompt + ".\n" + comp_prompt + builder_system_closing_instruction

        messages.append({"role": "system", "content": prompt})
        # Add few-shot examples to the message history
        messages = self.add_few_shot_examples(messages)

        messages.append({"role": "user", "content": goal + thinker_output})

        return messages

    def execute(self, goal, thinker_output, max_retry_times = 0):
        """
        Processes the output from the thinker model and prepares it for the constructor model.

        Parameters:
            - goal (str): the original goal of the user.
            - thinker_output (str): The output from the thinker model.

        Returns:
        - output_text (str): The processed output ready for the constructor model.
        :param **kwargs:
        """

        prompt = self.prepare_prompt(goal, thinker_output)
        output_text = self.call_model(prompt)

        #performing safeguarding
        if max_retry_times > 0:
            logger = logging.getLogger(f"{self.__class__.__name__}")
            logger.info("Safe Guarding Builder Model")
            # print("Safe Guarding Builder")
            for i in range(max_retry_times):
                if self.safe_guard(output_text):
                    return output_text
                logger.warning(f"DEBUG:: Builder Output Invalid, Retrying {i+1}/{max_retry_times}...")
                output_text = self.call_model(prompt) #TODO: alternative, keep this conversation with a follow up prompt, refering back to the map. or add a ending to the prompt to ensure different answer.
            return None
        return output_text

    def safe_guard(self, output):
        """
        safeguarding the output of the builder model, ensure that it is not output invalid component.
        :param output: a string of output to be checked
        :return: boolean, true or false for validity
        """
        components: list[str] = self.extract_downstream_components(output)
        logging.info(f"DEBUG:: Safe Guarding:: Extracted components {components}")
        if len(components) == 0:
            return False
        return all(component in self.component_map for component in components)

    def extract_downstream_components(self, input_string):
        components = set()  # avoid duplicates

        try:
            # full json
            data = json.loads(input_string)
            if "relationship" in data:
                for relation in data["relationship"]:
                    if "name" in relation:
                        components.add(relation["name"].split('@')[0])
                    if "downstream" in relation:
                        components.add(relation["downstream"].split('@')[0])
            return list(components)
        except Exception:
            lines = input_string.split('\n')
            for line in lines:
                try: # partial json
                    data = json.loads(line.strip('- _ ')) # Strip common list item markers and extra spaces before attempting JSON parse
                    if isinstance(data, dict) and "name" in data and "downstream" in data:
                        components.add(data["name"].split('@')[0])
                        components.add(data["downstream"].split('@')[0])
                except Exception:
                    #regex
                    name_pattern = r"name=([^;{}\n]+)"
                    downstream_pattern = r"downstream=([^;{}\n]+)"
                    name_matches = re.findall(name_pattern, line)
                    downstream_matches = re.findall(downstream_pattern, line)
                    for match in name_matches:
                        components.add(match.split('@')[0])
                    for match in downstream_matches:
                        components.add(match.split('@')[0])

        return list(components)


if __name__ == '__main__':
    c = BuilderModel("builder")
    thinker_output = "%This is the output from the thinker model%"
    d = c.prepare_prompt("Goal", thinker_output, )
    print(d)
