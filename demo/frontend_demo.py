from flask import Flask, render_template, request, jsonify, session
import json
import re
import ast

from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel
from cascade.safe_cascade_driver import SafeCascadeDriver
from cascade.thinker_model import ThinkerModel

from components.component_factory.component_factory import ComponentFactory
from components.component_factory.component_registry import ComponentRegistry
from schema.utils import validate_and_parse_cascade_output


app = Flask(__name__)
app.secret_key = '12345'


global_data = None

@app.route('/set')
def set_data(input):
    global global_data
    global_data = input
    return 'Data set!'

@app.route('/get')
def get_data():
    return global_data

thinker = ThinkerModel("gpt-3.5-turbo")
builder = BuilderModel("gpt-3.5-turbo")
constructor = ConstructorModel("gpt-3.5-turbo")

def filter_keys_and_values(input_dict):
    search_keywords = ["openaiagent", "promptbuilder"]
    filtered_dict = {key: value for key, value in input_dict.items()
                     for keyword in search_keywords
                     if keyword.lower() in key.lower()}
    return filtered_dict

def replace_user_input(data_dict, new_input):
    for key in data_dict:
        if 'user_input' in data_dict[key]:
            data_dict[key]['user_input'] = new_input
    return data_dict


def update_prompts(json_data, new_prompts):
    for item in json_data:
        item_id = item['id']
        if item_id in new_prompts:
            new_parameters = ast.literal_eval(new_prompts[item_id])
            item['parameters'].update(new_parameters)
    return json_data


@app.route('/')
def index():
    return render_template('index.html')

###############################################################################
#Student View

@app.route('/student')
def student():
    return render_template('student.html')
@app.route('/submit_student', methods=['POST'])
def submit_student():
    data = request.get_json()
    chat = data['inputText']
    print(chat)
    print("regenerating")
    with open('prompts/data.json', 'r') as file:
        factory_input = json.load(file)
    result = ""
    current_factory = get_data()
    if not current_factory:
        result = "Sorry there is no factory input yet."
    else:
        # factory_input = update_user_prompt(factory_input, chat)
        # setup_prompt = json.loads(factory_input)
        # registry = ComponentRegistry()
        # factory = ComponentFactory(registry)
        # factory.setup(setup_prompt)
        # print("Running factory....")
        # result = factory.run()
        # print("Result = \n" + result)
        # result = factory.run()
        # print("rerunning Result = \n" + result)
        # print("perished")
        # factory.perish()
        params = current_factory.get_user_params()
        print(params)
        updated = replace_user_input(params, chat)
        print(updated)
        current_factory.set_user_params(updated)
        set_data(current_factory)
        print("Running factory....")
        result = current_factory.run()
        print("Result = \n" + result)
        result = current_factory.run()
        print("rerunning Result = \n" + result)
        print("perished")
        current_factory.perish()
        result = current_factory.run()
        print("Result = \n" + result)
    return {
        'student_input': chat,
        'final_result': result
    }


###############################################################################
@app.route('/modify_prompt', methods=['POST'])
def modify_prompt():
    data = request.get_json()
    current_factory = get_data()
    factory_input = current_factory.get_modifiable_params()
    print("***************")
    print(factory_input)
    print(data)
    updated = dict(reversed(list(data.items())))
    print(type(updated))
    current_factory.update_modifiable_params(updated)
    set_data(current_factory)
    print(current_factory.get_modifiable_params())
    return jsonify(success=True, message='Prompt modified successfully.')

@app.route('/regenerate', methods=['POST'])
def regenerate():
    print("regenerating")
    with open('prompts/data.json', 'r') as file:
        factory_input = json.load(file)
    result = ""
    if not factory_input:
        result = "Sorry there is no factory input yet."
    else:
        current_factory = get_data()
        print(current_factory.get_modifiable_params())
        print("Running factory....")
        result = current_factory.run()
        print("Result = \n" + result)
        result = current_factory.run()
        print("rerunning Result = \n" + result)
        print("perished")
        current_factory.perish()
        result = current_factory.run()
        print("Result = \n" + result)

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
        driver = SafeCascadeDriver("gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo", max_retry_times=3)
        driver.execute(input_text)
        print(f"Final Thinker Output: {driver.thinker_output}")
        print(f"Final Builder Output: {driver.thinker_output}")
        print(f"Final Constructor Output: {driver.constructor_output}")

        thinker_output = driver.thinker_output
        builder_output = driver.builder_output
        constructor_output = driver.constructor_output

        # thinker_output_text = json.dumps(thinker_output)
        # builder_output_text = json.dumps(builder_output)
        constructor_output_text = json.dumps(validate_and_parse_cascade_output(constructor_output), indent=4)
        input_schemas = constructor_output
        print("Parsing schemas...")
        parsed_input_schemas = validate_and_parse_cascade_output(input_schemas)
        with open('prompts/data.json', 'w', encoding='utf-8') as f:
            json.dump(parsed_input_schemas, f, ensure_ascii=False, indent=4)

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
        # session['factory'] = factory
        # dictionary['factory'] = factory
        set_data(factory)
        print("success?")
        print("Result = \n" + result)
        params = factory.get_modifiable_params()

        result_list = [(key, str(value)) for key, value in params.items()]
        # print("-----")
        # print(result_list)
    return {
        'thinker_output': thinker_output,
        'builder_output': builder_output,
        'constructor_output': constructor_output_text,
        'final_result': result,
        'prompt_list': result_list
    }

if __name__ == '__main__':
    app.run(debug=True)
