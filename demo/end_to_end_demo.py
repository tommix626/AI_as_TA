"""
A demo that allows input to be fully generated to a working flow.
"""

from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel
from cascade.thinker_model import ThinkerModel

thinker = ThinkerModel("gpt-3.5-turbo")
builder = BuilderModel("gpt-3.5-turbo")
constructor = ConstructorModel("gpt-3.5-turbo")

# Define the initial input for the Thinker model
# initial_thinker_input = "Instructor: Do a summary for the newest 5 posts from Mastodon and send me a summary of those post with the role of a morning news reporter. I will listen to your summarization while eating breakfast"
initial_thinker_input = "Instructor: load the material in the file I saved at ./shared/content.txt. I will listen to its summarization while eating breakfast"
config = "you don't need an output component leave the final result in the final component is enough"
initial_thinker_input += config

thinker_output = thinker.execute(initial_thinker_input)
print("Thinker Output:", thinker_output)


builder_output = builder.execute(goal=initial_thinker_input, thinker_output=thinker_output)
print("Builder Output:", builder_output)


constructor_output = constructor.execute(goal=initial_thinker_input+thinker_output, builder_output = builder_output)
print("Constructor Output:", constructor_output)

from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry
from schema.utils import validate_and_parse_cascade_output

# schema of a flow that summarize the newest ten post to the user.
input_schemas = constructor_output



print("Parsing schemas...")
parsed_input_schemas = validate_and_parse_cascade_output(input_schemas)

print("Setting up factory....")
registry = ComponentRegistry()
factory = ComponentFactory(registry)
factory.setup(parsed_input_schemas)

print("Running factory....")
result = factory.run()
print("Result = \n" + result)