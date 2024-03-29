from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel
from cascade.thinker_model import ThinkerModel

thinker = ThinkerModel("gpt-3.5-turbo")
builder = BuilderModel("gpt-3.5-turbo")
constructor = ConstructorModel("gpt-3.5-turbo")

# Define the initial input for the Thinker model
initial_thinker_input = "Instructor: Do a summary for the newest 5 posts from Mastodon and send me a summary of those post with the role of a morning news reporter. I will listen to your summarization while eating breakfast"



thinker_output = thinker.execute(initial_thinker_input)
print("Thinker Output:", thinker_output)


builder_output = builder.execute(thinker_output)
print("Builder Output:", builder_output)


constructor_output = constructor.execute(builder_output)
print("Constructor Output:", constructor_output)
