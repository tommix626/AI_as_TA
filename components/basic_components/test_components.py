from components.base_component import BaseComponent


# In your component module (components.py or similar)
class TestComponentA(BaseComponent):
    component_schema = {"name": "TestComponentA", "inputs": [{"parameter": "input", "type": "string"}]}

class TestComponentB(BaseComponent):
    component_schema = {"name": "TestComponentB", "inputs": [{"parameter": "input", "type": "string"}]}

