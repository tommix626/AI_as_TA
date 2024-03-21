from collections import deque

from components.component_factory.define import component_map
def get_component_class(component_type):
    """Retrieve the component class from a pre-defined mapping."""

    return component_map.get(component_type) #component_map is in define.py

def topological_sort(graph, in_degree):
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
