from flask import Flask, render_template, request, jsonify
import json

from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel
from cascade.thinker_model import ThinkerModel
from schema.utils import validate_and_parse_cascade_output

app = Flask(__name__)

# Initialize models
thinker = ThinkerModel("gpt-3.5-turbo")
builder = BuilderModel("gpt-3.5-turbo")
constructor = ConstructorModel("gpt-3.5-turbo")

@app.route('/')
def index():
    # Just render the template on GET request.
    return render_template('index.html')

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
        # Process the input through the models
        thinker_output = thinker.execute(input_text)
        print(thinker_output)
        builder_output = builder.execute(goal=input_text, thinker_output=thinker_output)
        print(builder_output)
        constructor_output = constructor.execute(goal=input_text+thinker_output, builder_output=builder_output)
        print(constructor_output)
        # Prepare the output
        thinker_output_text = json.dumps(thinker_output, indent=4)
        builder_output_text = json.dumps(builder_output, indent=4)
        constructor_output_text = json.dumps(validate_and_parse_cascade_output(constructor_output), indent=4)

    return jsonify({
        'thinker_output': thinker_output_text,
        'builder_output': builder_output_text,
        'constructor_output': constructor_output_text
    })

if __name__ == '__main__':
    app.run(debug=True)
