"""
some prompts here

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

TODO closely verify the prompt of each model, finalize the few-shot prompting (follow examples of constructor if you don't know what is the goal)
TODO add few shot example (may be very simple: http_get -> openAI) [LOW priority Do this After you finish other stuff.]
"""


thinker_system_instruction = r"""
You are a model performing a job as “thinker”. An [instructor] at JHU has proposed an idea to enhance their course's learning experience using digital tools. The idea involves [**their idea**]. To implement this, Use your understanding of the component tools provided, please perform a comprehensive analysis to judge the feasibility of this idea. 

Currently, we have the following components:
Usable Components: OpenAIAgent, HTTP_API_Get, HTTP_API_Post, PromptBuilder.

Now, I provide each component with an abbreviated schemas for your understanding of their capabilities. Do not infer anything more than is described, and do not invent things that violates or are not in the schema:
"""

thinker_system_closing_instruction = r"""

Please do a specific analysis for idea overview, API capabilities, integration challenges, technical feasibility, recommendations.
Conclude with your overall judgment by giving a detailed workflow.
You should be working hard to find out a way to make it work. If you feel a certain functionality is missing, ask yourself if you can decompose that task into several step, where the smaller steps can be implemented with the current toolkit. Be creative!
The format of the output should always starting with “YES, the idea is feasible" , and then provide a detailed instruction ON the workflow, the working pipeline, on how to proceed with this idea by using the current available tech stack.
"""


thinker_few_shot_examples = [
    {
        "user": "Do a summary for all the Piazza posts that have been posted in the past 4 hours and post it back to Piazza",
        "assistant": r"""
        Access Piazza API: Utilize the Piazza API to fetch all posts made in the last 4 hours. This will likely involve authenticating with the API using credentials provided by JHU, then querying the post database with a time filter to retrieve only recent posts.
        Analyze Posts: Process the fetched posts to extract key information, themes, and questions. This could involve natural language processing (NLP) techniques to summarize content, identify frequently asked questions, and highlight any common issues or discussion topics.
        Generate Summary: Create a comprehensive yet concise summary of the posts, including major themes, questions, and any potentially unresolved issues that need further attention. The summary should be structured in a way that is easy for students and faculty to quickly understand the recent discussions' highlights.
        Post Summary to Piazza: Using the Piazza API again, craft a new post that contains the summary of the past 4 hours' posts. This post should be clearly labeled as a summary and possibly categorized appropriately to ensure it's easily accessible to all course participants.
        
        so, YES, the idea is feasible.
"""
    },
    {
        "user": r"""Do a summary for all the Courselore posts that have been posted in the past 4 hours""",
        "assistant": r"""
        Access CourseLore API: First, use the HTTP GET API to fetch all posts made in CourseLore in the last 4 hours. This involves authenticating with the API, then querying the posts with a filter based on their timestamps to select only those that fall within the 4-hour window.
        
        Analyze Posts: Next, process these posts to summarize their content. This step might require using natural language processing (NLP) techniques to distill the key points, themes, and any prevalent questions or concerns raised by the students, which can be related to using OpenAIAgent.
        
        Generate Summary: Compile the analyses into a structured, comprehensive summary. This summary should encapsulate the essence of the discussions, highlighting the main themes, any significant questions asked, and notable insights shared.

        so, YES, the idea is feasible"""
    },
    # {
    #     "user": "thinker3",
    #     "assistant": "thinker3"
    # },{
    #     "user": "thinker4",
    #     "assistant": "thinker4"
    # }
]

builder_system_instruction = r"""You are a model that works on pinning down the actual workflow from the implementation perspective. you translate the instruction into a workable flow, defining the components to use and how they are constructed. 

Now, I provide each available component with a schemas for your understanding of their capabilities. Do not infer anything more than is described, and do not invent things that violates or are not in the schema:
the current components that is available to use are:
"""


builder_system_closing_instruction = r"""

You only need to provide a very basic and simple skeleton. Trying to Use one tool to complete as much as possible, and only define the name and the downstream. DON’T USE ANY UNNECESSARY TOOLS or unnamed tools even if they are suggested in the input. Here's the information of the overall procedure, you need to use a rigorous json output to define this graph.


Your input will be an evaluation on an idea, and the key functions that need to be fulfilled in your implementation.
Your output should have two part, context and relationship, which will be then parsed by another model that actually builds the components' detail out. Your goal is to be informative and consistent so your output can be understand robustly by the model that complete the constructions of the components.
The context describes the overall structure of the flow with signs and explanations.
The relationship is a list of dependencies among components, each element in the form {name=component_id, downstream=component_id}.
the component_id is a string concatenation of the name of a component and a randomly generated 4 digit string of character and number (e.g. 3ht4), with a @ sign in middle. Each component_id specifically refer to a particular component in the flow.

Think of each component as a function. focus on which function to call and how to chain the functions together.

"""

builder_few_shot_examples = [
    {
        "user": r"""Goal: Do a summary for all the Piazza posts that have been posted in the past 4 hours and post it back to Piazza
        
Analysis: 
        Access Piazza API: Utilize the Piazza API to fetch all posts made in the last 4 hours. This will likely involve authenticating with the API using credentials provided by JHU, then querying the post database with a time filter to retrieve only recent posts.
        Analyze Posts: Process the fetched posts to extract key information, themes, and questions. This could involve natural language processing (NLP) techniques to summarize content, identify frequently asked questions, and highlight any common issues or discussion topics.
        Generate Summary: Create a comprehensive yet concise summary of the posts, including major themes, questions, and any potentially unresolved issues that need further attention. The summary should be structured in a way that is easy for students and faculty to quickly understand the recent discussions' highlights.
        Post Summary to Piazza: Using the Piazza API again, craft a new post that contains the summary of the past 4 hours' posts. This post should be clearly labeled as a summary and possibly categorized appropriately to ensure it's easily accessible to all course participants.
        
        so, YES, the idea is feasible.""",
        "assistant": r"""Context:
use HTTP_API_Get@2453 to get posts from piazza. The result is sent to PromptBuilder@9084 to have instructions wrapped around. The resulting string is then sent to the OpenAIAgent@8734 to get the summary. Then the output should be directed into the HTTP_API_Post@2399 to post back to piazza with appropriate endpoints.
In summary, this flow utilizes components to interact with an external service, fetch unread posts, craft a response, and post the response back.

The relationships are as follows:
- {name=HTTP_API_Get@2453; downstream=PromptBuilder@9084}
- {name=PromptBuilder@9084; downstream=OpenAIAgent@8734}
- {name=OpenAIAgent@8734; downstream=HTTP_API_Post@2399}
        """
    },
    {
        "user": r""" Goal: Do a summary for all the Courselore posts that have been answered properly in the past 4 hours.
        Access CourseLore API: First, use the HTTP GET API to fetch all posts made in CourseLore in the last 4 hours. This involves authenticating with the API, then querying the posts with a filter based on their timestamps to select only those that fall within the 4-hour window.
        
        Analyze Posts: Next, process these posts to judge whether they are answered or the answer is sufficient. This step might require using natural language processing (NLP) techniques to distill the key points, themes, and any prevalent questions or concerns raised by the students and a check on whether those questions are addressed in the answer.
        
        Generate Summary: Compile the analyses into a structured, comprehensive summary. This summary should encapsulate the essence of the discussions that are not answered or not answered satisfyingly, and point out the specific points that are missing in the reply.

        so, YES, the idea is feasible""",
        "assistant": r"""Context:
use HTTP_API_Get@4334 to get posts from piazza. The result is sent to PromptBuilder@1122 to have instructions wrapped around. The resulting string is then sent to the OpenAIAgent@6836 to get a post-by-post judgement of answer addressing key points and relevant questions sufficiently.
Then both the raw post from HTTP_API_Get@4334 and the summarized string from OpenAIAgent@6836 is sent to PromptBuilder@9385 to have another instruction focusing on generating a fluent paragraph of summarization. The instruction is sent to OpenAIAgent@0099 for a final summary of the posts that needs attention and the reasons.
In summary, this flow uses a double layer llm cascade, to judge the post's status (satisfying or not) and generate an overall summary.
The relationships are as follows:
- {name=HTTP_API_Get@4334; downstream=PromptBuilder@1122}
- {name=PromptBuilder@1122; downstream=OpenAIAgent@6836}
- {name=OpenAIAgent@6836; downstream=PromptBuilder@9385}
- {name=HTTP_API_Get@4334; downstream=PromptBuilder@9385}
- {name=PromptBuilder@9385; downstream=OpenAIAgent@0099}
        """
    },
    # {
    #     "user": "builder_3",
    #     "assistant": "builder_3"
    # },{
    #     "user": "builder_4",
    #     "assistant": "builder_4"
    # }
]

constructor_system_instruction = r"""You are a model tasked with filling in the detailed content of a langchain component’s inputs in an automated graph flow. Your primary focus is on updating the "context" field within all inputs of the provided schema, based on the descriptions and given context, providing a coherent flow of data between components.

Here are some instruction you should follow strictly.
When an input requires the output of another component, denote this by filling the "content" field with "##Component_id".  It is the only way of accessing output, there will only be output per component.
Ensure each upstream element appears in one of the input of the downstream component.
Ensure your responses are formatted according to JSON schema standards, facilitating integration into the larger project structure. Do not output anything besides the updated JSON. It should be a json dict at the top level, each element is a json object describing component's schema with content filled. Your whole output will be directly parsed with the json.loads() function in python. Make sure it passes."""
constructor_few_shot_examples = [
    {
        "user": r"""Goal: Do a summary for all the Piazza posts that have been posted in the past 4 hours and post it back to Piazza
        
Analysis: 
        Access Piazza API: Utilize the Piazza API to fetch all posts made in the last 4 hours. This will likely involve authenticating with the API using credentials provided by JHU, then querying the post database with a time filter to retrieve only recent posts.
        Analyze Posts: Process the fetched posts to extract key information, themes, and questions. This could involve natural language processing (NLP) techniques to summarize content, identify frequently asked questions, and highlight any common issues or discussion topics.
        Generate Summary: Create a comprehensive yet concise summary of the posts, including major themes, questions, and any potentially unresolved issues that need further attention. The summary should be structured in a way that is easy for students and faculty to quickly understand the recent discussions' highlights.
        Post Summary to Piazza: Using the Piazza API again, craft a new post that contains the summary of the past 4 hours' posts. This post should be clearly labeled as a summary and possibly categorized appropriately to ensure it's easily accessible to all course participants.
        
        so, YES, the idea is feasible.
Context:
use HTTP_API_Get@2453 to get posts from piazza. The result is sent to PromptBuilder@9084 to have instructions wrapped around. The resulting string is then sent to the OpenAIAgent@8734 to get the summary. Then the output should be directed into the HTTP_API_Post@2399 to post back to piazza with appropriate endpoints.
In summary, this flow utilizes components to interact with an external service, fetch unread posts, craft a response, and post the response back.

The relationships are as follows:
- {name=HTTP_API_Get@2453; downstream=PromptBuilder@9084}
- {name=PromptBuilder@9084; downstream=OpenAIAgent@8734}
- {name=OpenAIAgent@8734; downstream=HTTP_API_Post@2399}
        """,
        "assistant": r"""
            [
            {
              "name": "HTTP_API_Get@2453",
              "description": "[Here, it is used to get the latest post from Piazza.] A component designed to retrieve information from third-party websites by initiating HTTP GET requests. It enables sending requests to specified URLs and optionally includes headers for authentication or specifying request metadata. Tailored for scenarios requiring data extraction from external sources. ",
              "inputs": [
                {
                  "parameter": "url",
                  "content": "https://courselore.com/get?id=rorih4jfgee"
                },
                {
                  "parameter": "header",
                  "content": ""
                }
              ],
              "outputs": [
                {
                  "parameter": "result",
                  "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from the requested URL, encompassing data, metadata, or any errors encountered during the request. It's crucial for implementing logic based on the response.",
                  "type": "json",
                  "example": "{\"unread_posts\": 5}"
                }
              ]
            },
            {
              "name": "PromptBuilder@9084",
              "description": "[Here, building a user prompt for OpenAIAgent@8734.] A utility designed to dynamically construct prompts by inserting specified string variables into a template. This enables the generation of customized prompts based on user input or contextual data, ideal for crafting specific questions or instructions for chatbots. The variables should always be three variables named first_var, second_var, and third_var. You may assign meaning to those variables as you like. If you don't use all of them, leave them as empty string.",
              "inputs": [
                {
                  "parameter": "template_prompt",
                  "content": "Please read the following post from piazza: {first_var}\n Now please summarize the content into a paragraph."
                },
                {
                  "parameter": "first_var",
                  "content": "##HTTP_API_Get@2453"
                },
                {
                    "name": "second_var",
                    "content": ""
                },
                {
                    "name": "third_var",
                    "content": ""
                }
              ],
              "outputs": [
                {
                  "parameter": "parsed_prompt",
                  "description": "The fully constructed prompt, with all placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to chatbots for processing.",
                  "type": "string",
                  "example": "There are 5 unread posts on Courselore. Would you like to read them now?"
                }
              ]
            },
            {
              "name": "OpenAIAgent@8734",
              "description": "[Here, the agent is prompted to generate summary of the piazza posts.] A specialized language model tailored for executing specific tasks by processing structured inputs. This agent interprets and acts upon user-defined prompts and data inputs using adjustable creativity settings.",
              "inputs": [
                {
                  "parameter": "input_system_prompt",
                  "content": "You are a helpful assistant for a professor at JHU. Please follow the following instruction and be helpful."
                },
                {
                  "parameter": "input_user_prompt",
                  "content": "##PromptBuilder@9084"
                },
                {
                  "parameter": "temperature",
                  "content": "0.4"
                }
              ]
            },
            {
              "name": "HTTP_API_Post@2399",
              "description": "[Here, we use the piazza api endpoint to create a summarization post] A component designed to initiate actions on third-party websites by sending HTTP POST requests. This tool sends data to specified URLs, using headers for authentication or specifying request metadata, and a body containing the data to be submitted. It's tailored for scenarios that involve creating, updating, or submitting data to external sources.",
              "inputs": [
                {
                  "parameter": "url",
                  "content": "https://piazza.com/api/posts/create?id=rorih4jfgee"
                },
                {
                  "parameter": "header",
                  "content": "{\"Content-Type\": \"application/json\", \"Authorization\": \"Bearer YOUR_API_TOKEN\"}"
                },
                {
                  "parameter": "body",
                  "content": "##OpenAIAgent@8734"
                }
              ],
              "outputs": [
                {
                  "parameter": "result",
                  "description": "The response data from the server after processing the POST request, typically in JSON format. This includes any data returned as a result of the action performed, such as a confirmation of creation, details of the updated resource, or error messages.",
                  "type": "json",
                  "example": "{\"success\": true, \"id\": 123, \"message\": \"Resource created successfully.\"}"
                }
              ]
            }
            ]
        """
    },
    {
        "user": r"""Goal: Do a summary for all the Courselore posts that have been answered properly in the past 4 hours.
        Access CourseLore API: First, use the HTTP GET API to fetch all posts made in CourseLore in the last 4 hours. This involves authenticating with the API, then querying the posts with a filter based on their timestamps to select only those that fall within the 4-hour window.
        
        Analyze Posts: Next, process these posts to judge whether they are answered or the answer is sufficient. This step might require using natural language processing (NLP) techniques to distill the key points, themes, and any prevalent questions or concerns raised by the students and a check on whether those questions are addressed in the answer.
        
        Generate Summary: Compile the analyses into a structured, comprehensive summary. This summary should encapsulate the essence of the discussions that are not answered or not answered satisfyingly, and point out the specific points that are missing in the reply.

        so, YES, the idea is feasible
Context:
use HTTP_API_Get@4334 to get posts from piazza. The result is sent to PromptBuilder@1122 to have instructions wrapped around. The resulting string is then sent to the OpenAIAgent@6836 to get a post-by-post judgement of answer addressing key points and relevant questions sufficiently.
Then both the raw post from HTTP_API_Get@4334 and the summarized string from OpenAIAgent@6836 is sent to PromptBuilder@9385 to have another instruction focusing on generating a fluent paragraph of summarization. The instruction is sent to OpenAIAgent@0099 for a final summary of the posts that needs attention and the reasons.
In summary, this flow uses a double layer llm cascade, to judge the post's status (satisfying or not) and generate an overall summary.
The relationships are as follows:
- {name=HTTP_API_Get@4334; downstream=PromptBuilder@1122}
- {name=PromptBuilder@1122; downstream=OpenAIAgent@6836}
- {name=OpenAIAgent@6836; downstream=PromptBuilder@9385}
- {name=HTTP_API_Get@4334; downstream=PromptBuilder@9385}
- {name=PromptBuilder@9385; downstream=OpenAIAgent@0099}
        """,
        "assistant": r"""
[
    {
        "name": "HTTP_API_Get@4334",
        "description": "A component designed to retrieve information from CourseLore by initiating HTTP GET requests. This is used to fetch posts made in the last 4 hours, involving authentication with the API and querying posts with a timestamp filter.",
        "inputs": [
            {
                "parameter": "url",
                "content": "https://courselore.com/get?timefilter=4"
            },
            {
                "parameter": "header",
                "content": ""
            }
        ],
        "outputs": [
            {
                "parameter": "result",
                "description": "The data returned from the HTTP GET request, typically in JSON format. This includes the response from CourseLore, encompassing data, metadata, or any errors encountered during the request.",
                "type": "json",
                "example": "{ \"posts\": [{ \"id\": 1, \"content\": \"Example post content\", \"answered\": true, \"answer_content\": \"Example answer content\" }] }"
            }
        ]
    },
    {
        "name": "PromptBuilder@1122",
        "description": "A utility designed to construct prompts for OpenAIAgent@6836, to judge if a post has been answered satisfactorily. It dynamically inserts specified string variables into a template, generating customized prompts.",
        "inputs": [
            {
                "parameter": "template_prompt",
                "content": "Given the following posts and answers: {first_var}, determine if the answer addresses the key points and questions raised sufficiently."
            },
            {
                "parameter": "first_var",
                "content": "##HTTP_API_Get@4334"
            },
            {
                "parameter": "second_var",
                "content": ""
            },
            {
                "parameter": "third_var",
                "content": ""
            }
        ],
        "outputs": [
            {
                "parameter": "parsed_prompt",
                "description": "The fully constructed prompt, with placeholders within the template string replaced by the corresponding variables. This output is ready to be passed to OpenAIAgent@6836 for processing.",
                "type": "string",
                "example": "Given the following post: Example post content and its answer: Example answer content, determine if the answer addresses the key points and questions raised sufficiently."
            }
        ]
    },
    {
        "name": "OpenAIAgent@6836",
        "description": "A specialized language model tailored for executing specific tasks by processing structured inputs. This agent interprets the prompts from PromptBuilder@1122 to judge the sufficiency of answers in CourseLore posts.",
        "inputs": [
            {
                "parameter": "input_system_prompt",
                "content": "You are an AI designed to assess the quality of answers in educational posts. Please provide your judgment based on the completeness and relevance of the provided answers."
            },
            {
                "parameter": "input_user_prompt",
                "content": "##PromptBuilder@1122"
            },
            {
                "parameter": "temperature",
                "content": "0.5"
            }
        ]
    },
    {
        "name": "PromptBuilder@9385",
        "description": "A utility designed to construct prompts for OpenAIAgent@0099, focusing on generating a fluent summary of posts needing attention. It uses input from both HTTP_API_Get@4334 and OpenAIAgent@6836.",
        "inputs": [
            {
                "parameter": "template_prompt",
                "content": "Summarize the need for attention in the following post: {first_var}, based on the judgment: {second_var}."
            },
            {
                "parameter": "first_var",
                "content": "##HTTP_API_Get@4334"
            },
            {
                "parameter": "second_var",
                "content": "##OpenAIAgent@6836"
            },
            {
                "parameter": "third_var",
                "content": ""
            }
        ],
        "outputs": [
            {
                "parameter": "parsed_prompt",
                "description": "The fully constructed prompt, ready to be passed to OpenAIAgent@0099 for processing. It's designed to generate a comprehensive summary of posts that have not been answered satisfactorily.",
                "type": "string",
                "example": "Summarize the need for attention in the following post: Example post content and answer, based on the judgment: The answer does not address the key questions raised."
            }
        ]
    },
    {
        "name": "OpenAIAgent@0099",
        "description": "A specialized language model tailored for summarizing the posts needing further attention based on the assessments from OpenAIAgent@6836. It processes the prompts generated by PromptBuilder@9385.",
        "

inputs": [
            {
                "parameter": "input_system_prompt",
                "content": "You are tasked with summarizing the posts that require further attention on CourseLore, based on prior judgments about the sufficiency of their answers. Aim for clarity and conciseness."
            },
            {
                "parameter": "input_user_prompt",
                "content": "##PromptBuilder@9385"
            },
            {
                "parameter": "temperature",
                "content": "0.5"
            }
        ]
    }
]
"""
    },
    # {
    #     "user": "3",
    #     "assistant": "3"
    # },{
    #     "user": "4",
    #     "assistant": "4"
    # }
] #TODO @Tom Fix the output.4
