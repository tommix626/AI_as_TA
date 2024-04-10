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


# TODOS:
- constructors should separate the id and the name into two fields. (replaced with @ symbol system)
- Now we are using string as the passing, there should be also a version which generate a langchain Runnable chain as the end output using LCEL.
- add schema for each component
- output doesn't need to contain "outputs" field or need to be specific to the context.
- emphasis on no chinese character? quotes especially, and no missing comma for example field (probably a few shot mistake)
- IMP: define schema strictly: at raw stage, parsed stage, etc...
- Need thinker's description to be more conceptual, when the component number get larger, we don't want to bombard thinker with so many detailed code, but to focus on its ability to select the correct components to use. (on TEST 2)
- Tom change the prompt so that no extra character like \n and spaces are eliminated from the few-shot result.
- the post and get api endpoints need to have a specification of the result's format.

# Documentation for adding component
- to generate a new component, create a derived class from BaseComponent, and update the `component_map` in `components/define.py` to include the tool into the prompt cascade chain.


# TEST Cascade

```
"Instructor: Do a summary for all the Courselore posts that have been posted in the past 4 hours and send an email to every students about this summary"
Thinker Output: 
        NO, the idea is infeasible

        The current tech stack does not include a specific tool for sending emails directly to students. To implement this idea successfully, an email sending service or SMTP API would be necessary, which is not provided in the available components. Additional tools capable of handling email functionalities would be required for the seamless execution of this task.
Builder Output: {
 "error": "Email functionality not supported with the existing components. Additional tools are required for sending emails directly to students."
}
Constructor Output: {
    "error": "Email functionality not supported with the existing components. Additional tools are required for sending emails directly to students."
}
```

```
"Instructor: Do a summary for the newest 5 posts from Mastodon and send me a summary of those post with the role of a morning news reporter. I will listen to your summarization while eating breakfast"

Thinker Output: 
        NO, the idea is infeasible

        The current toolkit provided does not include a direct integration with the Mastodon social network API (HTTP_API_Get does not have a predefined Mastodon endpoint). To summarize the newest 5 posts from Mastodon, we would need a specific tool or API designed for interacting with Mastodon's data. 

        To achieve this idea feasibly, additional components capable of interfacing with Mastodon's API or similar social media platforms would be required. These tools could provide access to the recent posts, facilitate their analysis, and assist in generating a morning news reporter-style summary for the instructor.
Builder Output: {
  "error": "Additional components for Mastodon API integration are required for the feasibility of this idea. The current toolkit does not support direct interaction with the Mastodon social network API."
}
Constructor Output: {
    "error": "Additional components for Mastodon API integration are required for the feasibility of this idea. The current toolkit does not support direct interaction with the Mastodon social network API."
}
```

# After re-prompting
- eliminate infeasible option
```
Thinker Output:   Access Mastodon API: Begin by using the HTTP API Get component to retrieve the five most recent posts from Mastodon. Use the provided endpoint for retrieving recent public posts and specify a limit of 5 to get the latest posts.

  Analyze Mastodon Posts: Process the retrieved Mastodon posts to extract essential information, trending topics, or noteworthy events. Utilize NLP techniques to understand the content and themes of the posts effectively.

  Generate Morning News Summary: Craft a compelling and informative summary of the five newest Mastodon posts, reflecting the role of a morning news reporter. Start with a brief introduction, provide key highlights from each post, and conclude with a wrap-up of the overall sentiment or trending topics.

  Deliver Summary: Once the summary is prepared, you can present it as a detailed morning news report to the instructor, capturing the essence of the Mastodon posts in a digestible and engaging manner.

  Using the components available, it is feasible to execute this task by integrating data retrieval, analysis, and storytelling to deliver a news reporter-style summary of the latest Mastodon posts.
Builder Output: Context:
Use HTTP_API_Get@5478 to fetch the 5 most recent posts from Mastodon. The retrieved data is then passed to OpenAIAgents@8321 for analysis of the posts' content and themes. The analyzed information is sent to PromptBuilder@8765 to construct a morning news report-style summary, which is the final result.
In summary, this flow retrieves Mastodon posts, analyzes their content, generates a news report-style summary, and delivers the summary.

Relationships:
- {name=HTTP_API_Get@5478; downstream=OpenAIAgents@8321}
- {name=OpenAIAgents@8321; downstream=PromptBuilder@8765}
Constructor Output: 
[
    {
        "name": "HTTP_API_Get@5478",
        "description": "A component designed to retrieve information from the Mastodon social network by initiating HTTP GET requests. It fetches the five most recent posts from Mastodon using the specified endpoint and limit parameters.",
        "inputs": [
            {
                "parameter": "url",
                "content": "https://mastodon.social/api/v1/timelines/public?limit=5"
            },
            {
                "parameter": "headers",
                "content": ""
            }
        ],
        "outputs": [
            {
                "parameter": "result",
                "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the Mastodon social network, encompassing data, metadata, or any errors encountered.",
                "type": "json",
                "example": "{ \"posts\": [{ \"id\": 1, \"content\": \"Example post content 1\" }] }"
            }
        ]
    },
    {
        "name": "OpenAIAgents@8321",
        "description": "A specialized language model tailored for analyzing content and themes of received posts. It processes and extracts essential information from the retrieved Mastodon posts.",
        "inputs": [
            {
                "parameter": "input_system_prompt",
                "content": "Analyzing the content and themes of the most recent Mastodon posts to extract key information and trending topics."
            },
            {
                "parameter": "input_user_prompt",
                "content": "##HTTP_API_Get@5478"
            },
            {
                "parameter": "temperature",
                "content": "0.3"
            }
        ]
    },
    {
        "name": "PromptBuilder@8765",
        "description": "A utility designed to construct a morning news report-style summary from the analyzed Mastodon posts. It formats the information for a news reporter presentation.",
        "inputs": [
            {
                "parameter": "template_prompt",
                "content": "Good morning! This is your news reporter with the latest updates. Today's headlines from Mastodon: {var1}. Now for the detailed news highlights: {var2}. Concluding with trending topics and sentiments from Mastodon posts."
            },
            {
                "parameter": "var1",
                "content": "##HTTP_API_Get@5478"
            },
            {
                "parameter": "var2",
                "content": "##OpenAIAgents@8321"
            },
            {
                "parameter": "var3",
                "content": ""
            }
        ]
    }
]
```
Output:
```
Parsing schemas...
Attempted to access stale output. Triggering run.
Schema validation passed.
LLM output validation passed.
Setting up factory....
Running factory....
Result = 
Good morning! This is your news reporter with the latest updates. Today's headlines from Mastodon: Based on the most recent Mastodon posts:

1. **Weather Alert**: The National Weather Service Office in Mount Holly, New Jersey, extended a Flood Warning for Hunterdon and Somerset counties until April 4, 12:00 AM EDT. The post includes a link to the warning details and an image related to the alert.

2. **Agriculture News**: The Ministry of Agriculture, Forestry, and Fisheries in Japan announced the "April's Bargain Vegetables," highlighting a versatile vegetable for spring. The post includes a link to the article and various hashtags related to agriculture and vegetables.

3. **Traffic Updates**: A bot account provides real-time updates on bridge travel times in Ciudad Juárez, Mexico, including travel times to different locations and a link to a website for more information. The post includes images of different bridges in the area.

4. **Sports News**: A bot account shares information about the Georgia football team's spring safety depth chart, linking to an article for more details. The post includes an image related to the football team.

5. **College Football News**: ESPN reports that former New York Giants coach Joe Judge has joined the staff at Ole Miss. The post includes a link to the article and is categorized under College Football. The post mentions the official ESPN Flipboard profile.

These posts cover a range of topics including weather alerts, agriculture news, traffic updates, sports news, and college football updates.. Now for the detailed news highlights: Based on the most recent Mastodon posts:

1. **Weather Alert**: The National Weather Service Office in Mount Holly, New Jersey, extended a Flood Warning for Hunterdon and Somerset counties until April 4, 12:00 AM EDT. The post includes a link to the warning details and an image related to the alert.

2. **Agriculture News**: The Ministry of Agriculture, Forestry, and Fisheries in Japan announced the "April's Bargain Vegetables," highlighting a versatile vegetable for spring. The post includes a link to the article and various hashtags related to agriculture and vegetables.

3. **Traffic Updates**: A bot account provides real-time updates on bridge travel times in Ciudad Juárez, Mexico, including travel times to different locations and a link to a website for more information. The post includes images of different bridges in the area.

4. **Sports News**: A bot account shares information about the Georgia football team's spring safety depth chart, linking to an article for more details. The post includes an image related to the football team.

5. **College Football News**: ESPN reports that former New York Giants coach Joe Judge has joined the staff at Ole Miss. The post includes a link to the article and is categorized under College Football. The post mentions the official ESPN Flipboard profile.

These posts cover a range of topics including weather alerts, agriculture news, traffic updates, sports news, and college football updates.. Concluding with trending topics and sentiments from Mastodon posts.

```
