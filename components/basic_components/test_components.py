from components.base_component import BaseComponent


# In your component module (components.py or similar)
class TestComponentA(BaseComponent):
    component_schema = {"name": "TestComponentA", "inputs": [{"parameter": "input", "type": "string"}]}
    def __init__(self, component_id, input):
        super().__init__(component_id)
        self.input = input
        self.cnt=0

    def run(self):
        self.cnt+=1
        self.output = f"TestComponentA ran, cnt={self.cnt}"

class TestComponentB(BaseComponent):
    component_schema = {"name": "TestComponentB", "inputs": [{"parameter": "input", "type": "string"}]}
    def __init__(self, component_id, input):
        super().__init__(component_id)
        self.input = input
        self.cnt=0

    def run(self):
        self.cnt+=1
        self.output = f"TestComponentB ran, cnt={self.cnt}"

