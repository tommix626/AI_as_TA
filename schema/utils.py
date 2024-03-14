import json

def convert_json_to_dict(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e.msg}")
        return None
