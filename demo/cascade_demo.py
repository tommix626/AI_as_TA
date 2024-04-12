import json

from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel
from cascade.thinker_model import ThinkerModel
from schema.utils import validate_and_parse_cascade_output, save_schema_to_file

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

#try parsing, if pass, then save it.

validate_and_parse_cascade_output(constructor_output)

save_schema_to_file(constructor_output,"../tmp/cascade_output.json")
# with open("../tmp/cascade_output.json", "w") as outfile:
#     json.dump(constructor_output, outfile)
print("done")

