
import pytest

from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry

# Mock schemas to simulate the input to ComponentFactory
schemas = [
    {"id": "A", "name": "TestComponentA", "parameters": {"input": "value for A"}},
    {"id": "B", "name": "TestComponentB", "parameters": {"input": "##A"}},
]


# Test case for successful component creation and dependency resolution
def test_successful_component_creation_and_dependency_resolution():
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)
    sorted_component_ids = factory.parse_and_sort_dependencies(schemas)

    # Assuming 'parse_and_sort_dependencies' also initializes the components
    # Verify the components are registered and sorted correctly
    assert "A" in registry.components and "B" in registry.components
    assert sorted_component_ids == ["A", "B"]  # Adjust based on actual logic

    # Verify dependency setup
    component_a = registry.get("A")
    component_b = registry.get("B")
    assert callable(component_b.parameters["input"])  # Assuming parameters are stored and input is a callback


# Test case for detecting cyclic dependencies
def test_cyclic_dependency_detection():
    cyclic_schemas = [
        {"id": "A", "name": "TestComponentA", "parameters": {"input": "##B"}},
        {"id": "B", "name": "TestComponentB", "parameters": {"input": "##A"}},
    ]
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)

    # Expect the cyclic dependency detection to raise a ValueError
    with pytest.raises(ValueError):
        factory.parse_and_sort_dependencies(cyclic_schemas)

# Further tests can be added to cover more scenarios...
