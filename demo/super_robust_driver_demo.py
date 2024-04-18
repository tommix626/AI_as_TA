import logging

from cascade.safe_cascade_driver import SafeCascadeDriver
from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry
from schema.utils import validate_and_parse_cascade_output

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

driver = SafeCascadeDriver("gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo",max_retry_times=3)
instructor_input = ("Instructor: load the material in the file I saved at ./shared/content.txt. I will listen to "
                    "its summarization while eating breakfast you don't need an output component leave the final "
                    "result in the final component is enough")
driver.execute(instructor_input)
print("\n\n\n*******************************************************************************\n\n")
print(f"Final Thinker Output: {driver.thinker_output}")
print(f"Final Builder Output: {driver.thinker_output}")
print(f"Final Constructor Output: {driver.constructor_output}")


# running the flow
input_schemas = driver.constructor_output



print("Parsing schemas...")
parsed_input_schemas = validate_and_parse_cascade_output(input_schemas)

print("Setting up factory....")
registry = ComponentRegistry()
factory = ComponentFactory(registry)
factory.setup(parsed_input_schemas)

print("Running factory....")
result = factory.run()
print("Result = \n" + result)


result = factory.run()
print("rerunning Result = \n" + result)

print("perished")
factory.perish()
result = factory.run()
print("Result = \n" + result)