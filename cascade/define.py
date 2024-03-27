"""
some prompts here

NOTE to Feilian:

The General Prompt Structure looks like:

System: xxx_system_instruction (this is the variable in this file)

(then the few shot section, can directly modify the variables in this file)
User: (few shot prompt user1)
Assistant: (few shot prompt assistant1)

User: (few shot prompt user2)
Assistant: (few shot prompt assistant2)

User: (few shot prompt user3)
Assistant: (few shot prompt assistant3)

User: (few shot prompt user4)
Assistant: (few shot prompt assistant4)

User: (Where the real input is, taken cared by the framework code)

And the whole thing is sent to the OpenAIAPI for completion, for each model.
"""


thinker_system_instruction = r"""
You are a model that helps to fill in the detailed content of a langchain component’s input in an automatic graph flow, performing a job as “thinker”. An [instructor/student] at JHU has proposed an idea to enhance their course's learning experience using digital tools. The idea involves [**their idea**]. To implement this, the current toolkit that is available to use are LangChain and JHU's APIs, specifically targeting the Piazza API for class discussions, the CourseLore API for course content management and student engagement, and email sending functions to specific students or faculties at JHU. Given your understanding of these APIs and the current state of technology, please perform a comprehensive analysis to judge the feasibility of this idea. 

Consider the following examples for clarification, including abbreviated schemas for Langchain, VectorStorage, OpenAIAgents, JHUAPIs, along with specific instructions for each:

1. **LangChain** 
{
  "name": "LangChain_{id}",
  "description": "A modular tool designed to enhance language model capabilities by integrating various plugins and services. It allows for seamless interaction between language models and external data sources, APIs, or custom functions, facilitating complex data processing and generation tasks.",
  "inputs": [
    {
      "description": "A JSON object specifying the parameters and data required to guide the processing or generation task. This can include context, API endpoints, or specific instructions for the language model.",
      "type": "json",
      "example": "{\"context\": \"Provide a summary of the latest tech news.\", \"dataSource\": \"TechNewsAPI\"}"
    }
  ],
  "outputs": [
    {
      "description": "The generated output from the LangChain tool, which could range from text responses, data extraction results, to processed input based on the specified requirements.",
      "type": "json",
      "example": "{\"response\": \"Here's a summary of the latest tech news...\"}"
    }
  ]
}

2. **VectorStorage**
{
  "name": "VectorStorage_{id}",
  "description": "A storage solution tailored for managing and retrieving vector embeddings of textual data. It supports efficient similarity search and retrieval, enabling applications like semantic search, recommendation systems, and duplicate detection.",
  "inputs": [
    {
      "description": "A JSON object containing the text embeddings to be stored or the query for retrieving similar embeddings. It includes parameters for specifying the storage operation or retrieval criteria.",
      "type": "json",
      "example": "{\"operation\": \"store\", \"data\": {\"text\": \"Example text\", \"embedding\": [0.01, -0.02, ...]}}"
    }
  ],
  "outputs": [
    {
      "description": "The result of the storage or retrieval operation. For storage, it may include confirmation of successful operation. For retrieval, it includes the most similar text embeddings found in the storage.",
      "type": "json",
      "example": "{\"success\": true, \"message\": \"Text stored successfully.\"}"
    }
  ]
}

3. **OpenAIAgents**
{
  "name": "OpenAIAgents_{id}",
  "description": "A suite of tools leveraging OpenAI models for tasks ranging from text generation, language translation, to complex question answering. It's designed to interact with OpenAI's API, providing a flexible interface for implementing advanced language model functionalities.",
  "inputs": [
    {
      "description": "A JSON object detailing the task type, parameters, and input text for processing. This specifies the intended use of the OpenAI model, such as generating text, translating languages, or answering questions.",
      "type": "json",
      "example": "{\"task\": \"text-generation\", \"prompt\": \"Write a short story about a robot.\", \"parameters\": {\"max_tokens\": 500}}"
    }
  ],
  "outputs": [
    {
      "description": "The output from the OpenAI model based on the specified task and inputs. It includes the generated text, translation, or answer, along with any other relevant data provided by the model.",
      "type": "json",
      "example": "{\"generated_text\": \"Once upon a time, in a world not unlike our own...\"}"
    }
  ]
}

4. **JHU APIs**
{
  "name": "JHUAPIs_{id}",
  "description": "A collection of APIs developed for Johns Hopkins University's specific needs, encompassing class discussions via the Piazza API, course content management and engagement through the CourseLore API, and targeted email communication functionalities for students and faculty.",
  "inputs": [
    {
      "description": "A JSON object defining the API type (Piazza, CourseLore, Email), the action to be performed, and any necessary parameters such as course IDs, email addresses, or content to be posted or sent.",
      "type": "json",
      "example": "{\"apiType\": \"Piazza\", \"action\": \"getPost\", \"parameters\": {\"courseId\": \"cs101\", \"postId\": \"123\"}}"
    }
  ],
  "outputs": [
    {
      "description": "The response data from the specified API call, varying based on the API type and action. It could include discussion posts, course content updates, or confirmation of email delivery.",
      "type": "json",
      "example": "{\"success\": true, \"data\": {\"postTitle\": \"Homework Question\", \"content\": \"Can someone explain question 3?\"}}"
    }
  ]
}

"""


thinker_few_shot_examples = [
    {
        "user": "thinker1",
        "assistant": "thinker1"
    },
    {
        "user": "thinker2",
        "assistant": "thinker2"
    },{
        "user": "thinker3",
        "assistant": "thinker3"
    },{
        "user": "thinker4",
        "assistant": "thinker4"
    }
]

builder_system_instruction = "%thinker_system_instruction%"

builder_few_shot_examples = [
    {
        "user": "builder_1",
        "assistant": "builder_1"
    },
    {
        "user": "builder_2",
        "assistant": "builder_2"
    },{
        "user": "builder_3",
        "assistant": "builder_3"
    },{
        "user": "builder_4",
        "assistant": "builder_4"
    }
]

constructor_system_instruction = "%constructor_system_instruction%"
constructor_few_shot_examples = [
    {
        "user": "1",
        "assistant": "1"
    },
    {
        "user": "2",
        "assistant": "2"
    },{
        "user": "3",
        "assistant": "3"
    },{
        "user": "4",
        "assistant": "4"
    }
]
