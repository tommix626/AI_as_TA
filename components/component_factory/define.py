from components.basic_components.OpenAI_Agent import OpenAIAgentComponent
from components.basic_components.test_components import TestComponentA, TestComponentB

# component map used by the factory, it should be the output name used by the constructor.
component_map = {
            # Mapping of component type names to their classes Name appeared in LLM Orchestration Output:classes.
            "OpenAIAgent": OpenAIAgentComponent,
            # Include other mappings for tests
            "TestComponentA": TestComponentA,
            "TestComponentB": TestComponentB,
}