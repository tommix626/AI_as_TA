class ComponentRecord:
    def __init__(self, name, component_id, parameters=None):
        """
        Initializes a new instance of ComponentRecord.

        :param name: The name of the component.
        :param component_id: The unique identifier for the component.
        :param parameters: A list of parameters for the component, each with its content.
                           Each parameter in the list is a dictionary with keys like 'parameter' and 'content'.
        """
        self.name = name
        self.component_id = component_id
        self.parameters = parameters if parameters is not None else []

    @classmethod
    def from_raw_schema(cls, schema):
        """
        Class method to create a ComponentRecord instance from a raw schema segment.

        :param schema: A python dictionary representing a part of the raw orchestration output schema
                       pertaining to a single component.
        :return: An instance of ComponentRecord initialized with the data from the schema.
        """
        # Extract necessary information from the schema
        name = schema.get("name", "")
        component_id = schema.get("id", "")
        parameters = schema.get("parameters", [])

        # Convert parameters to a list of dictionaries with 'parameter' and 'content' keys
        parameter_list = [{"parameter": key, "content": value} for key, value in parameters.items()]

        return cls(name, component_id, parameter_list)
