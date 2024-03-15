import logging


class ComponentFactory:
    def __init__(self, registry):
        self.registry = registry

    def create_component(self, schema):
        """Create a component based on the schema."""
        component_type = schema["name"]
        component_id = schema["id"]

        # Retrieve the component class from its type
        component_cls = self._get_component_class(component_type)
        if not component_cls:
            logging.error(f"Component type {component_type} not recognized.")
            return None

        # Validate schema inputs against the component's expected inputs
        if not self._validate_schema_inputs(schema, component_cls.component_schema):
            logging.error(f"Schema validation failed for component {component_type}.")
            return None

        # Instantiate component with parameters and register it
        component = component_cls(component_id=component_id, global_registry=self.registry, **schema["parameters"])
        self._setup_dependencies(component, schema["parameters"])
        self.registry.register(component)

        return component

    def _get_component_class(self, component_type):
        """Retrieve the component class from a global or local mapping."""
        component_map = {
            # Mapping of component type names to their classes
            "OpenAIAgent": OpenAIAgentComponent,
            # Include other mappings...
        }
        return component_map.get(component_type)

    def _validate_schema_inputs(self, schema, component_schema):
        """Validate the provided schema inputs against the component's expected inputs."""
        expected_params = {param["parameter"] for param in component_schema["inputs"]}
        provided_params = set(schema["parameters"].keys())

        return expected_params == provided_params

    def _setup_dependencies(self, component, parameters):
        """Setup dependencies for the component based on its parameters."""
        for param_name, param_value in parameters.items():
            if isinstance(param_value, str) and param_value.startswith("##"):
                upstream_id = param_value[2:]
                upstream_component = self.registry.get(upstream_id)
                if upstream_component:
                    # Setup callback or direct assignment as needed
                    callback = lambda: upstream_component.get_output()
                    setattr(component, param_name, callback)
                else:
                    logging.warning(f"Upstream component {upstream_id} not found for {param_name}.")
            else:
                # Direct assignment for non-dependency parameters
                setattr(component, param_name, param_value)
