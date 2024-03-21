import json


def _parse_llm_generated_schema(generated_schema):
    """
    further manipulate the dict converted from raw json string input.
    :param generated_schema: a json conversion of component descriptions generated by the LLM chain
    :return: a list of component dict (name,id,inputs,outputs)
    """
    components = []
    for component in generated_schema:
        component_name, component_id = component["name"].split('_')
        comp_details = {
            "name": component_name, #name used for finding the class
            "id": component["name"], #unique id, in the form ClassName_{4 char id}
            "inputs": {},
            "outputs": {}
        }
        for input_param in component.get("inputs", []):
            comp_details["inputs"][input_param["parameter"]] = input_param.get("content", "")
        for output_param in component.get("outputs", []):
            comp_details["outputs"][output_param["parameter"]] = output_param.get("content", "")
        components.append(comp_details)
    return components

def _convert_json_to_dict(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e.msg}")
        return None