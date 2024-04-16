from flask import Flask, render_template, request, jsonify
import json

from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel
from cascade.thinker_model import ThinkerModel

from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry
from schema.utils import validate_and_parse_cascade_output

app = Flask(__name__)

thinker = ThinkerModel("gpt-3.5-turbo")
builder = BuilderModel("gpt-3.5-turbo")
constructor = ConstructorModel("gpt-3.5-turbo")

@app.route('/')
def index():
    with open('prompts/user_thinker.txt', 'w') as file:
        pass
    with open('prompts/user_builder.txt', 'w') as file:
        pass
    with open('prompts/user_constructor.txt', 'w') as file:
        pass
    with open('prompts/thinker.txt', 'r') as file:
        thinker = file.read()
    with open('prompts/builder.txt', 'r') as file:
        builder = file.read()
    with open('prompts/constructor.txt', 'r') as file:
        constructor = file.read()
    return render_template('index.html', thinker = thinker, builder = builder, constructor = constructor)

@app.route('/modify_prompt', methods=['POST'])
def modify_prompt():
    data = request.get_json()
    user_think = data.get('user_think', '')
    with open('prompts/user_thinker.txt', 'w') as file:
        file.write(user_think)
    user_build = data.get('user_build', '')
    with open('prompts/user_builder.txt', 'w') as file:
        file.write(user_build)
    user_construct = data.get('user_construct', '')
    with open('prompts/user_constructor.txt', 'w') as file:
        file.write(user_construct)
    # Return a response to the client (optional)
    return jsonify(success=True, message='Prompt modified successfully.')

@app.route('/regenerate', methods=['POST'])
def regenerate():
    print("regenerating")
    with open('prompts/factory_input.txt', 'r') as file:
        factory_input = file.read()
    result = ""
    if(factory_input == ""):
        result = "Sorry there is no factory input yet."
    else:
        try:
            registry = ComponentRegistry()
            factory = ComponentFactory(registry)
            factory.setup(factory_input)

            print("Running factory....")
            result = factory.run()
            print("Result = \n" + result)
        except:
            result = "Those are the workflows. Sorry we don't have specific output for now. Thank you for using it."

    return {
        'final_result': result
    }


@app.route('/process', methods=['POST'])
def process_input():
    thinker_output_text = ""
    builder_output_text = ""
    constructor_output_text = ""
    if request.method == 'POST':
        data = request.get_json()
        input_text = data['inputText']
        config = "you don't need an output component leave the final result in the final component is enough"
        input_text += config
        print("running!")

        with open('prompts/thinker.txt', 'r') as file:
            thinker_prompt = file.read()
        with open('prompts/builder.txt', 'r') as file:
            builder_prompt = file.read()
        with open('prompts/constructor.txt', 'r') as file:
            constructor_prompt = file.read()

        print(thinker_prompt == "")
        thinker_output = thinker.execute(input_text, thinker_prompt)

        print(thinker_output)
        builder_output = builder.execute(goal=input_text, thinker_output=thinker_output, user_prompting = builder_prompt)
        print(builder_output)
        constructor_output = constructor.execute(goal=input_text+thinker_output, builder_output=builder_output, user_prompting = constructor_prompt)
        print(constructor_output)

        thinker_output_text = json.dumps(thinker_output, indent=4)
        builder_output_text = json.dumps(builder_output, indent=4)
        constructor_output_text = json.dumps(validate_and_parse_cascade_output(constructor_output), indent=4)
        input_schemas = constructor_output

        print("Parsing schemas...")
        parsed_input_schemas = validate_and_parse_cascade_output(input_schemas)

        print("Setting up factory....")
        try:
            with open('prompts/factory_input.txt', 'w') as file:
                file.write(parsed_input_schemas)
            registry = ComponentRegistry()
            factory = ComponentFactory(registry)
            factory.setup(parsed_input_schemas)

            print("Running factory....")
            result = factory.run()
            print("Result = \n" + result)
        except:
            result = "Those are the workflows. Sorry we don't have specific output for now. Thank you for using it."

    return {
        'thinker_output': thinker_output,
        'builder_output': builder_output,
        'constructor_output': constructor_output_text,
        'final_result': result

        # 'thinker_output': thinker_output,
        # 'builder_output': "dummy",
        # 'constructor_output': "dummy",
        # 'final_result': "dummy"
    }

if __name__ == '__main__':
    app.run(debug=True)
