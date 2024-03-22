import pytest

from components.define import component_map
from schema._parse import _convert_json_to_dict


@pytest.mark.parametrize("component_name, component_class", component_map.items())
def test_component_schema_not_none(component_name, component_class):
    if(component_name.startswith("Test")):
        return #ignore Test Components
    schema = getattr(component_class, "component_schema", None)
    assert schema is not None, f"{component_name} does not have a 'component_schema' static variable."
    dict_result = _convert_json_to_dict(schema)
    assert dict_result is not None, f"_convert_json_to_dict returned None for {component_name}'s schema."
