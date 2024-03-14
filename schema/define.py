# required schema for a component, used mainly by the constructor model.
predefined_component_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "inputs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "parameter": {"type": "string"},
                    "description": {"type": "string"},
                    "type": {"type": "string"},
                    "example": {"type": "string"},
                },
                "required": ["parameter", "description", "type"],
                "additionalProperties": False,
            },
        },
        "outputs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "parameter": {"type": "string"},
                    "description": {"type": "string"},
                    "type": {"type": "string"},
                    "example": {"type": "string"},
                },
                "required": ["parameter", "description", "type"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["name", "inputs", "outputs"],
    "additionalProperties": False,
}

# the return value of llm output.
llm_output_validation_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "inputs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "parameter": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["parameter", "content"],
                    "additionalProperties": True
                }
            },
            "outputs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "parameter": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["parameter", "content"],
                    "additionalProperties": True
                }
            },
        },
        "required": ["name", "inputs", "outputs"],
        "additionalProperties": True
    }
}
