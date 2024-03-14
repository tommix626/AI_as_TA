# AI_as_TA
Demo/Testing for the AI_as_TA project around No-code LLMOps

- `demos/context_langChain.ipynb` contains example of a TA bot for Data Structure using Information Retrieval.
- `langchain_demo.ipynb` contains demo of using the langchain library.
- `chroma_demo.ipynb` contains demo for using Chroma as Embedding Storage.


# No-code Runner Based on LLM Orchestration

A Bigger scale demo focusing on providing a NLP way to build flows automatically.


### Step 1: Schema Parsing
- **Goals:**
  - Read and validate JSON schemas.
  - Identify components and their dependencies.
- **Technical Details:**
  - Use Python’s `json` module to load and parse the schema.
  - Validate schema structure using a library like `jsonschema` to ensure it meets expected format, including required fields for each component (e.g., `name`, `inputs`, `outputs`).
  - Create a dependency graph to resolve execution order, possibly utilizing a directed graph and a library like `networkx` for dependency resolution.

### Step 2: Component Library Development
- **Goals:**
  - Develop a set of predefined components.
  - Standardize component interface for inputs/outputs.
- **Technical Details:**
  - Define each component as a Python class or function with a consistent interface, ensuring they can accept inputs and provide outputs in a standardized format.
  - Implement components for core functionalities required by your demo (e.g., HTTP GET/POST, PromptBuilder). Use external libraries like `requests` for HTTP operations.
  - Ensure each component can report errors and handle exceptions gracefully, returning a standard error format when necessary.

### Step 3: Constructing the Flow
- **Goals:**
  - Dynamically construct and execute the workflow from the schema.
  - Manage the state to pass data between components.
- **Technical Details:**
  - Based on the dependency graph, use a method to execute components in the correct order. This could be a simple linear execution for acyclic graphs or more complex scheduling for graphs with dependencies.
  - Implement a state management system to hold intermediate outputs. This could be a dictionary mapping component names to their outputs, which can then be passed as inputs to subsequent components.
  - For each component execution, dynamically map inputs from the schema or the state management system to the component’s parameters, execute the component, and update the state with its output.

### Step 4: Testing and Validation
- **Goals:**
  - Ensure individual components work as expected.
  - Validate the entire flow execution with a sample schema.
- **Technical Details:**
  - Write unit tests for each component using a framework like `pytest`, testing various input scenarios and error handling.
  - Create integration tests that validate the parsing, construction, and execution of a workflow using a predefined schema, ensuring the system behaves as expected end-to-end.

### Step 5: Execution Environment Setup
- **Goals:**
  - Create a simple execution environment to run your demo.
- **Technical Details:**
  - Set up a Python virtual environment to manage dependencies.
  - Ensure all external libraries needed for your components and workflow execution are included in your `requirements.txt` file.
  - Create a main script (`main.py`) that takes a schema as input (from a file or hardcoded for the demo), parses it, constructs the workflow, and executes it, displaying the final output.

By focusing on these streamlined steps, you'll be able to build a functional demo of your no-code platform, demonstrating the core capabilities of parsing schemas, executing defined components, and dynamically constructing flows based on input schemas.