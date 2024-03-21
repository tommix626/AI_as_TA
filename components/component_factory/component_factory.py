import logging

from collections import defaultdict, deque

from components.component_factory.component_registry import ComponentRegistry
from components.component_factory.utils import get_component_class, topological_sort


def _validate_inputs(schema, component_schema):
    """Validate the provided schema inputs against the component's expected inputs.
    Making sure no input is missing."""
    expected_params = {param["parameter"] for param in component_schema["inputs"]}
    provided_params = set(schema["parameters"].keys())

    return expected_params == provided_params


def _parse_and_sort_dependencies(components: list[dict[str,str]]) -> list[str]:
    """Parses dependencies and returns a list of component IDs in topological order.
    :param components: a parsed_cascade_output containing a list of components' schema.
    :return: a list of id of component in order.
    """
    graph = defaultdict(list)
    in_degree = defaultdict(int)  # Keep track of in-degrees for topological sort

    # Parse dependencies to construct the graph
    for component in components:
        component_id = component["id"]
        for param in component.get("parameters", {}).values():
            if isinstance(param, str) and param.startswith("##"):
                dependency_id = param[2:]
                graph[dependency_id].append(component_id)
                in_degree[component_id] += 1

    # Perform topological sort
    return topological_sort(graph, in_degree)


class ComponentFactory:
    """
    a factory is a representation over a single flow/graph.
    """

    def __init__(self, registry: ComponentRegistry):
        self.registry = registry  # factory will populate this registry with components and dependency.

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
        component = component_cls(component_id=component_id, **cascade_component_content_schema["parameters"])
        self._setup_component_dependencies(component, cascade_component_content_schema["parameters"])
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
                return False


        return True
