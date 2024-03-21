import logging

from components.component_factory.define import component_map
from collections import defaultdict, deque


class ComponentFactory:
    """
    a factory is a representation over a single flow/graph.
    """
    def __init__(self, registry):
        self.registry = registry # factory will populate this registry with components and dependency.

    def create_component(self, cascade_component_schema):
        """Create a component based on the schema. Schema is the output of the llm orchestration"""
        component_type = cascade_component_schema["name"]
        component_id = cascade_component_schema["id"]

        # Retrieve the component class from its type
        component_cls = self._get_component_class(component_type)
        if not component_cls:
            logging.error(f"Component type {component_type} not recognized.")
            return None

        # Validate schema inputs against the component's expected inputs
        if not self._validate_schema_inputs(cascade_component_schema, component_cls.component_schema):
            logging.error(f"Schema validation failed for component {component_type}.")
            return None

        # Instantiate component with parameters and register it
        component = component_cls(component_id=component_id, **cascade_component_schema["parameters"])
        self._setup_dependencies(component, cascade_component_schema["parameters"])
        self.registry.register(component)

        return component

    def _get_component_class(self, component_type):
        """Retrieve the component class from a pre-defined mapping."""

        return component_map.get(component_type) #component_map is in define.py

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
                    logging.warning(f"Upstream component ID= {upstream_id} not found when setting up param: {param_name}.")
            else:
                # Direct assignment for non-dependency parameters
                setattr(component, param_name, param_value)

    def setup(self, parsed_cascade_output):
        """
        Set up the graph for this flow from raw_cascade_output
        :param raw_cascade_output: caller should call validate_and_parse_cascade_output to make sure the input is conforming to the schema.
        :return:
        """
        # components = validate_and_parse_cascade_output(raw_cascade_output, llm_output_validation_schema)
        sorted_components = self._parse_and_sort_dependencies(parsed_cascade_output)
        for component in sorted_components:
            self._setup_dependencies(component,)


    def _parse_and_sort_dependencies(self, components):
        """Parses dependencies and returns a list of component IDs in topological order."""
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
        return self._topological_sort(graph, in_degree)

    def _topological_sort(self, graph, in_degree):
        """Performs a topological sort on the dependency graph."""
        queue = deque([node for node in graph if in_degree[node] == 0])
        sorted_order = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)

            for adjacent in graph[node]:
                in_degree[adjacent] -= 1
                if in_degree[adjacent] == 0:
                    queue.append(adjacent)

        if len(sorted_order) == len(graph):
            return sorted_order
        else:
            raise ValueError("A cyclic dependency was detected among the components.")