from components.basic_components.Document_Loader import DocumentLoaderComponent
from components.basic_components.HTTP_API_Get import HTTPGetComponent
from components.basic_components.HTTP_API_Post import HTTPPostComponent
from components.basic_components.Knowledge_Query import KnowledgeQueryComponent
from components.basic_components.OpenAI_Agent import OpenAIAgentComponent
from components.basic_components.Prompt_Builder import PromptBuilderComponent
from components.basic_components.User_input import UserInputComponent
from components.basic_components.test_components import TestComponentA, TestComponentB

# component map used by the factory, it should be the output name used by the constructor.
component_map = {
    # Mapping of component type names to their classes Name appeared in LLM Orchestration Output.  Cascade_output_str : class.
    "OpenAIAgent": OpenAIAgentComponent,
    "HTTP_API_Post": HTTPPostComponent,
    "HTTP_API_Get": HTTPGetComponent,
    "PromptBuilder": PromptBuilderComponent,
    "KnowledgeQuery": KnowledgeQueryComponent,
    "DocumentLoader": DocumentLoaderComponent,
    "UserInput": UserInputComponent,

    # Include other mappings for tests
    "TestComponentA": TestComponentA,
    "TestComponentB": TestComponentB,
}