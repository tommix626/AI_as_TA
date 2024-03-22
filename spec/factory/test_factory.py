import pytest

from components.component_factory.component_factory import ComponentFactory, _parse_and_sort_dependencies
from components.component_factory.component_registry import ComponentRegistry

# Mock schemas to simulate the input to ComponentFactory (cascade output after parsing)
schemas = [
    {"name": "TestComponentA", "id": "TestComponentA@1", "parameters": {"input": "value for A"}},
    {"name": "TestComponentB", "id": "TestComponentB@1", "parameters": {"input": "##TestComponentA@1"}},
]


schemas_complicate = [
    {"name": "TestComponentA", "id": "TestComponentA@1", "parameters": {"input": "value for A@1"}},
    {"name": "TestComponentB", "id": "TestComponentB@1", "parameters": {"input": "##TestComponentA@1"}},
    {"name": "TestComponentB", "id": "TestComponentB@2", "parameters": {"input": "##TestComponentA@8"}},
    {"name": "TestComponentA", "id": "TestComponentA@3", "parameters": {"input": "##TestComponentB@1"}},
    {"name": "TestComponentA", "id": "TestComponentA@8", "parameters": {"input": "##TestComponentA@3"}},
]
 # A@1 <- B@1 <- A@3 <- A@8 <- B@2


# Test case for successful component creation and dependency resolution
def test_successful_dependency_resolution():
    sorted_component_ids = _parse_and_sort_dependencies(schemas)

    # Assuming 'parse_and_sort_dependencies' also initializes the components
    # Verify the components are  sorted correctly
    assert sorted_component_ids == ["TestComponentA@1", "TestComponentB@1"]


def test_basic_factory_setup():
    """test if component is registered and callback is inserted"""
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)
    factory.setup(schemas)
    assert "TestComponentA@1" in registry.components and "TestComponentB@1" in registry.components
    # Verify dependency setup
    component_a = registry.get("TestComponentA@1")
    component_b = registry.get("TestComponentB@1")
    assert component_a is not None
    assert component_b is not None
    assert callable(component_b.input)


# Test case for detecting cyclic dependencies
def test_invalid_reference_name():
    cyclic_schemas = [
        {"name": "TestComponentA", "id": "TestComponentA@1", "parameters": {"input": "##Something@1"}},
        {"name": "TestComponentB", "id": "TestComponentB@1", "parameters": {"input": "##SomethingElse"}},
    ]
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)

    # Expect the wrong ref name detection to raise a ValueError
    with pytest.raises(ValueError):
        _parse_and_sort_dependencies(cyclic_schemas)

def test_cyclic_dependency_detection():
    cyclic_schemas = [
        {"name": "TestComponentA", "id": "TestComponentA@1", "parameters": {"input": "##ConeTestCompntB@1"}},
        {"name": "TestComponentB", "id": "TestComponentB@1", "parameters": {"input": "##ConeTestCompntA@1"}},
    ]
    registry = ComponentRegistry()
    factory = ComponentFactory(registry)

    # Expect the cyclic dependency detection to raise a ValueError
    with pytest.raises(ValueError):
        _parse_and_sort_dependencies(cyclic_schemas)