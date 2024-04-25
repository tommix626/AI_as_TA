import json
import logging

from collections import defaultdict, deque
from typing import Dict, Any

from components.base_component import BaseComponent
from components.component_factory.component_registry import ComponentRegistry
from components.component_factory.utils import get_component_class, topological_sort
from env import global_api_keys_and_config
from schema._parse import _convert_json_to_dict


def _validate_inputs(schema: dict, component_schema_str: str):
    """Validate the provided schema inputs against the component's expected inputs.
    Making sure no input is missing."""
    component_schema = _convert_json_to_dict(component_schema_str)
    expected_params = {param["parameter"] for param in component_schema["inputs"]}
    provided_params = set(schema["parameters"].keys())

    return expected_params == provided_params


def _parse_and_sort_dependencies(components: list[dict[str, str]]) -> list[str]:
    """Parses dependencies and returns a list of component IDs in topological order.
    Raises ValueError if an invalid dependency is found.

    :param components: a parsed_cascade_output containing a list of components' schema.
    :return: a list of id of component in order.
    """
    graph = defaultdict(list)
    in_degree = defaultdict(int)  # Keep track of in-degrees for topological sort
    component_ids = {component["id"] for component in components}  # Collect all component IDs for validation

    # Parse dependencies to construct the graph
    for component in components:
        component_id = component["id"]
        for param_value in component["parameters"].values():
            if isinstance(param_value, str) and param_value.startswith("##"):
                dependency_id = param_value[2:]
                if dependency_id not in component_ids:
                    raise ValueError(f"Invalid dependency ID '{dependency_id}' in component '{component_id}'.")
                graph[dependency_id].append(component_id)
                in_degree[component_id] += 1

    # Perform topological sort
    sorted_ids = topological_sort(graph, in_degree)

    # Verify all components are included in the sort (catches isolated nodes)
    if set(sorted_ids) != component_ids:
        raise ValueError("Not all components are connected in the dependency graph.")

    return sorted_ids


def api_endpoint_identifier(func):
    def wrapper(*args, **kwargs):
        print(f"Calling the API function {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Done calling API function {func.__name__}")

        return result

    return wrapper


class ComponentFactory:
    """
    a factory is a representation over a single flow/graph.
    """
    user_params: dict[str, str]
    entry_component: BaseComponent

    def __init__(self, registry: ComponentRegistry):
        self.registry = registry  # factory will populate this registry with components and dependency.
        self.entry_component = None
        self.user_params = {} #contains the extra parameters that are dynamically set by the user (setting, user_input etc.)

    def create_component(self, cascade_component_content_schema):
        """Create a component based on the schema. Schema is the output of the llm orchestration"""
        component_type = cascade_component_content_schema["name"]
        component_id = cascade_component_content_schema["id"]

        # Retrieve the component class from its type
        component_cls = get_component_class(component_type)
        if not component_cls:
            logging.error(f"Create Component: Component type {component_type} not recognized.")
            return None

        # Validate schema inputs against the component's expected inputs
        if not _validate_inputs(cascade_component_content_schema, component_cls.component_schema):
            logging.error(f"Create Component: Schema Inputs validation failed for component {component_type}.")
            return None

        # Instantiate component with parameters and register it
        component = component_cls(component_id=component_id, **cascade_component_content_schema["parameters"],**global_api_keys_and_config)
        self._setup_component_dependencies(component, cascade_component_content_schema["parameters"]) #set up the callbacks here
        self.registry.register(component)

        return component

    def _setup_component_dependencies(self, component, parameters):
        """Setup dependencies for the component based on its parameters.
        Updating "##" references with callback functions (get_output function of upstream component). """
        for param_name, param_value in parameters.items():
            if isinstance(param_value, str) and param_value.startswith("##"):
                upstream_id = param_value[2:]
                upstream_component = self.registry.get(upstream_id)
                if upstream_component:
                    # Setup callback or direct assignment as needed
                    callback = lambda: upstream_component.get_output()
                    setattr(component, param_name, callback)
                    component.add_dependency(upstream_component)
                else:
                    logging.warning(
                        f"Upstream component ID= {upstream_id} not found when setting up param: {param_name}.")
            else:
                # Direct assignment for non-dependency parameters
                setattr(component, param_name, param_value)

    def setup(self, parsed_cascade_output: list[dict]) -> bool:
        """
        Set up the graph for this flow from parsed_cascade_output.
        :param parsed_cascade_output: Caller should ensure the input conforms to the schema.
        :return: True if setup is successful, False otherwise.
        """
        # Map component IDs to their schemas for quick access
        component_schemas_by_id = {component["id"]: component for component in parsed_cascade_output}

        # Perform topological sort to determine the order for setting up components
        sorted_components_id = _parse_and_sort_dependencies(parsed_cascade_output)

        # Iterate over sorted component IDs and set up each component
        for component_id in sorted_components_id:
            component_schema = component_schemas_by_id.get(component_id)
            # sanity check for the topo sort algorithm
            if not component_schema:
                logging.error(f"Setup (Internal Error): Component schema for ID={component_id} not found.")
                raise RuntimeError

            if self.create_component(component_schema) is None:
                logging.error(f"Component creation error, component_id={component_id}.")
                return False


        # last one should be the entry point of the flow.
        self.entry_component = self.registry.get(sorted_components_id[-1])
        return True

    def run(self):
        return self.entry_component.get_output()

    def perish(self):
        self.entry_component.perish()


    @api_endpoint_identifier
    def get_modifiable_params(self):
        """
        Gathers and returns all modifiable parameters from each component registered in the factory's registry.

        Returns:
            str: A JSON-formatted string containing all components' modifiable parameters.
                 Each component's modifiable parameters are indexed by their component_id.
        """
        all_params = {}
        for component_id, component in self.registry.components.items():
            all_params[component_id] = component.modifiable_params

        print("$$$$$$$$$$$$$")
        print(all_params)
        # Convert the dictionary to a JSON-formatted string to standardize the output format

        return all_params


    @api_endpoint_identifier
    def update_modifiable_params(self, updates):
        """
        Updates modifiable parameters across multiple components based on provided updates.

        Args:
            updates (dict): A dictionary where keys are component IDs and values are dictionaries
                            of parameter names and their new values.
        """
        for component_id, params in updates.items():
            component = self.registry.get(component_id)
            if component:
                component.update_modifiable_params(params)
            else:
                logging.warning(f"No component found with ID {component_id} for update.")

    @api_endpoint_identifier
    def get_user_params(self):
        return {"user_input":"placeholder text"}

    @api_endpoint_identifier
    def set_user_params(self, updates):
        self.user_params = updates
