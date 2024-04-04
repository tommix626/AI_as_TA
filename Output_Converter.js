const fs = require('fs');

function generateJson(inputArray) {
  const nodeMappings = {
    "openai": {
      "width": 300,
      "height": 574,
      "id": "openAI_0",
      "position": {"x": 513.3297923232442, "y": -112.67554802812833},
      "type": "customNode",
      "data": {
        "id": "openAI_0",
        "label": "OpenAI",
        "version": 3,
        "name": "openAI",
        "type": "OpenAI",
        "baseClasses": [
          "OpenAI",
          "BaseLLM",
          "BaseLanguageModel"
        ],
        "category": "LLMs",
        "description": "Wrapper around OpenAI large language models",
        "inputParams": [
          {
            "label": "Connect Credential",
            "name": "credential",
            "type": "credential",
            "credentialNames": [
              "openAIApi"
            ],
            "id": "openAI_0-input-credential-credential"
          },
          {
            "label": "Model Name",
            "name": "modelName",
            "type": "options",
            "options": [
              {
                "label": "gpt-3.5-turbo-instruct",
                "name": "gpt-3.5-turbo-instruct"
              },
              {
                "label": "babbage-002",
                "name": "babbage-002"
              },
              {
                "label": "davinci-002",
                "name": "davinci-002"
              }
            ],
            "default": "gpt-3.5-turbo-instruct",
            "optional": true,
            "id": "openAI_0-input-modelName-options"
          },
          {
            "label": "Temperature",
            "name": "temperature",
            "type": "number",
            "default": 0.7,
            "optional": true,
            "id": "openAI_0-input-temperature-number"
          },
          {
            "label": "Max Tokens",
            "name": "maxTokens",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-maxTokens-number"
          },
          {
            "label": "Top Probability",
            "name": "topP",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-topP-number"
          },
          {
            "label": "Best Of",
            "name": "bestOf",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-bestOf-number"
          },
          {
            "label": "Frequency Penalty",
            "name": "frequencyPenalty",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-frequencyPenalty-number"
          },
          {
            "label": "Presence Penalty",
            "name": "presencePenalty",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-presencePenalty-number"
          },
          {
            "label": "Batch Size",
            "name": "batchSize",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-batchSize-number"
          },
          {
            "label": "Timeout",
            "name": "timeout",
            "type": "number",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-timeout-number"
          },
          {
            "label": "BasePath",
            "name": "basepath",
            "type": "string",
            "optional": true,
            "additionalParams": true,
            "id": "openAI_0-input-basepath-string"
          }
        ],
        "inputAnchors": [
          {
            "label": "Cache",
            "name": "cache",
            "type": "BaseCache",
            "optional": true,
            "id": "openAI_0-input-cache-BaseCache"
          }
        ],
        "inputs": {
          "modelName": "gpt-3.5-turbo-instruct",
          "temperature": 0.7,
          "maxTokens": "",
          "topP": "",
          "bestOf": "",
          "frequencyPenalty": "",
          "presencePenalty": "",
          "batchSize": "",
          "timeout": "",
          "basepath": ""
        },
        "outputAnchors": [
          {
            "id": "openAI_0-output-openAI-OpenAI|BaseLLM|BaseLanguageModel",
            "name": "openAI",
            "label": "OpenAI",
            "type": "OpenAI | BaseLLM | BaseLanguageModel"
          }
        ],
        "outputs": {},
        "selected": false
      },
      "selected": false,
      "positionAbsolute": {
        "x": 513.3297923232442,
        "y": -112.67554802812833
      },
      "dragging": false
    },
    "llmchain": {
      "width": 300,
      "height": 507,
      "id": "llmChain_0",
      "position": {"x": 1238.61656537962, "y": 236.5239307299537},
      "type": "customNode",
      "data": {
        "id": "llmChain_0",
        "label": "LLM Chain",
        "version": 3,
        "name": "llmChain",
        "type": "LLMChain",
        "baseClasses": [
          "LLMChain",
          "BaseChain",
          "Runnable"
        ],
        "category": "Chains",
        "description": "Chain to run queries against LLMs",
        "inputParams": [
          {
            "label": "Chain Name",
            "name": "chainName",
            "type": "string",
            "placeholder": "Name Your Chain",
            "optional": true,
            "id": "llmChain_0-input-chainName-string"
          }
        ],
        "inputAnchors": [
          {
            "label": "Language Model",
            "name": "model",
            "type": "BaseLanguageModel",
            "id": "llmChain_0-input-model-BaseLanguageModel"
          },
          {
            "label": "Prompt",
            "name": "prompt",
            "type": "BasePromptTemplate",
            "id": "llmChain_0-input-prompt-BasePromptTemplate"
          },
          {
            "label": "Output Parser",
            "name": "outputParser",
            "type": "BaseLLMOutputParser",
            "optional": true,
            "id": "llmChain_0-input-outputParser-BaseLLMOutputParser"
          },
          {
            "label": "Input Moderation",
            "description": "Detect text that could generate harmful output and prevent it from being sent to the language model",
            "name": "inputModeration",
            "type": "Moderation",
            "optional": true,
            "list": true,
            "id": "llmChain_0-input-inputModeration-Moderation"
          }
        ],
        "inputs": {
          "model": "{{openAI_0.data.instance}}",
          "prompt": "{{promptTemplate_0.data.instance}}",
          "outputParser": "",
          "inputModeration": "",
          "chainName": ""
        },
        "outputAnchors": [
          {
            "name": "output",
            "label": "Output",
            "type": "options",
            "description": "",
            "options": [
              {
                "id": "llmChain_0-output-llmChain-LLMChain|BaseChain|Runnable",
                "name": "llmChain",
                "label": "LLM Chain",
                "description": "",
                "type": "LLMChain | BaseChain | Runnable"
              },
              {
                "id": "llmChain_0-output-outputPrediction-string|json",
                "name": "outputPrediction",
                "label": "Output Prediction",
                "description": "",
                "type": "string | json"
              }
            ],
            "default": "llmChain"
          }
        ],
        "outputs": {
          "output": "llmChain"
        },
        "selected": false
      },
      "width": 300,
      "height": 507,
      "positionAbsolute": {
        "x": 1238.61656537962,
        "y": 236.5239307299537
      },
      "selected": false,
      "dragging": false
    },
    "prompttemplate": {
      "width": 300,
      "height": 332,
      "id": "promptTemplate_0",
      "position": {"x": 737.6394286633716, "y": 508.81332946461566},
      "type": "customNode",
      "data": {
        "id": "promptTemplate_0",
        "label": "Prompt Builder",
        "version": 1,
        "name": "promptTemplate",
        "type": "PromptTemplate",
        "baseClasses": [
          "PromptTemplate",
          "BaseStringPromptTemplate",
          "BasePromptTemplate",
          "Runnable"
        ],
        "category": "Prompts",
        "description": "Build Prompts",
        "inputParams": [
          {
            "label": "Format Prompt Values",
            "name": "promptValues",
            "type": "json",
            "optional": true,
            "acceptVariable": true,
            "list": true,
            "id": "promptTemplate_0-input-promptValues-json"
          }
        ],
        "inputAnchors": [
          {
            "label": "Template",
            "name": "template",
            "type": "RequestsGet",
            "rows": 4,
            "acceptVariable": true,
            "id": "promptTemplate_0-input-template-RequestsGet"
          }
        ],
        "inputs": {
          "template": "{{requestsGet_0.data.instance}}",
          "promptValues": ""
        },
        "outputAnchors": [
          {
            "id": "promptTemplate_0-output-promptTemplate-PromptTemplate|BaseStringPromptTemplate|BasePromptTemplate|Runnable",
            "name": "promptTemplate",
            "label": "PromptTemplate",
            "description": "Build Prompts",
            "type": "PromptTemplate | BaseStringPromptTemplate | BasePromptTemplate | Runnable"
          }
        ],
        "outputs": {},
        "selected": false
      },
      "width": 300,
      "height": 332,
      "selected": false,
      "positionAbsolute": {
        "x": 737.6394286633716,
        "y": 508.81332946461566
      },
      "dragging": false
    },
    "httpget": {
      "width": 300,
      "height": 251,
      "id": "requestsGet_0",
      "position": {"x": 262.78344978631833, "y": 507.092836787525},
      "type": "customNode",
      "data": {
        "id": "requestsGet_0",
        "label": "Requests Get",
        "version": 1,
        "name": "requestsGet",
        "type": "RequestsGet",
        "baseClasses": [
          "RequestsGet",
          "Tool",
          "StructuredTool",
          "Runnable"
        ],
        "category": "Tools",
        "description": "Execute HTTP GET requests",
        "inputParams": [
          {
            "label": "URL",
            "name": "url",
            "type": "string",
            "description": "Agent will make call to this exact URL. If not specified, agent will try to figure out itself from AIPlugin if provided",
            "additionalParams": true,
            "optional": true,
            "id": "requestsGet_0-input-url-string"
          },
          {
            "label": "Description",
            "name": "description",
            "type": "string",
            "rows": 4,
            "default": "A portal to the internet. Use this when you need to get specific content from a website. \nInput should be a  url (i.e. https://www.google.com). The output will be the text response of the GET request.",
            "description": "Acts like a prompt to tell agent when it should use this tool",
            "additionalParams": true,
            "optional": true,
            "id": "requestsGet_0-input-description-string"
          },
          {
            "label": "Headers",
            "name": "headers",
            "type": "json",
            "additionalParams": true,
            "optional": true,
            "id": "requestsGet_0-input-headers-json"
          }
        ],
        "inputAnchors": [],
        "inputs": {
          "url": "",
          "description": "A portal to the internet. Use this when you need to get specific content from a website. \nInput should be a  url (i.e. https://www.google.com). The output will be the text response of the GET request.",
          "headers": ""
        },
        "outputAnchors": [
          {
            "id": "requestsGet_0-output-requestsGet-RequestsGet|Tool|StructuredTool|Runnable",
            "name": "requestsGet",
            "label": "RequestsGet",
            "description": "Execute HTTP GET requests",
            "type": "RequestsGet | Tool | StructuredTool | Runnable"
          }
        ],
        "outputs": {},
        "selected": false
      },
      "width": 300,
      "height": 251,
      "selected": false,
      "positionAbsolute": {
        "x": 262.78344978631833,
        "y": 507.092836787525
      },
      "dragging": false
    },
    "httppost": {
      "width": 300,
      "height": 230,
      "id": "getVariable_0",
      "position": {"x": 1659.5733274449049, "y": 436.13449089592643},
      "type": "customNode",
      "data": {
        "id": "getVariable_0",
        "label": "HTTP Post",
        "version": 1,
        "name": "getVariable",
        "type": "GetVariable",
        "baseClasses": [
          "GetVariable",
          "Utilities"
        ],
        "category": "Utilities",
        "description": "HTTP Post: it should be a function that links to the outside",
        "inputParams": [],
        "inputAnchors": [
          {
            "label": "TODO: Function",
            "name": "TODO: Function",
            "type": "LLMChain",
            "placeholder": "var1",
            "acceptVariable": true,
            "id": "getVariable_0-input-TODO: Function-LLMChain"
          }
        ],
        "inputs": {
          "TODO: Function": "{{llmChain_0.data.instance}}"
        },
        "outputAnchors": [
          {
            "id": "getVariable_0-output-getVariable-GetVariable|Utilities",
            "name": "getVariable",
            "label": "GetVariable",
            "description": "HTTP Post: it should be a function that links to the outside",
            "type": "GetVariable | Utilities"
          }
        ],
        "outputs": {},
        "selected": false
      },
      "width": 300,
      "height": 230,
      "selected": false,
      "positionAbsolute": {
        "x": 1659.5733274449049,
        "y": 436.13449089592643
      },
      "dragging": false
    }
  };

  function linkComponents(components) {
    const links = [];
    
    const hasHTTPGET = components.includes('HTTPGET');
    const hasPromptTemplate = components.includes('prompttemplate');
    const hasLLMChain = components.includes('llmchain');
    const hasHTTPPost = components.includes('HTTPPost');
    const hasOpenAI = components.includes('openai');

    if (hasHTTPGET && hasPromptTemplate) {
        links.push({
            source: "requestsGet_0",
            sourceHandle: "requestsGet_0-output-requestsGet-RequestsGet|Tool|StructuredTool|Runnable",
            target: "promptTemplate_0",
            targetHandle: "promptTemplate_0-input-template-RequestsGet",
            type: "buttonedge",
            id: "requestsGet_0-requestsGet_0-output-requestsGet-RequestsGet|Tool|StructuredTool|Runnable-promptTemplate_0-promptTemplate_0-input-template-RequestsGet"
        });
    }
    if (hasLLMChain && hasHTTPPost) {
      links.push({
        source: "llmChain_0",
        sourceHandle: "llmChain_0-output-llmChain-LLMChain|BaseChain|Runnable",
        target: "getVariable_0",
        targetHandle: "getVariable_0-input-TODO: Function-LLMChain",
        type: "buttonedge",
        id: "llmChain_0-llmChain_0-output-llmChain-LLMChain|BaseChain|Runnable-getVariable_0-getVariable_0-input-TODO: Function-LLMChain"
      });
    }

    if (hasOpenAI && hasPromptTemplate && hasLLMChain) {
        links.push({
            source: "openAI_0",
            sourceHandle: "openAI_0-output-openAI-OpenAI|BaseLLM|BaseLanguageModel",
            target: "llmChain_0",
            targetHandle: "llmChain_0-input-model-BaseLanguageModel",
            type: "buttonedge",
            id: "openAI_0-openAI_0-output-openAI-OpenAI|BaseLLM|BaseLanguageModel-llmChain_0-llmChain_0-input-model-BaseLanguageModel"
        });
        links.push({
            source: "promptTemplate_0",
            sourceHandle: "promptTemplate_0-output-promptTemplate-PromptTemplate|BaseStringPromptTemplate|BasePromptTemplate|Runnable",
            target: "llmChain_0",
            targetHandle: "llmChain_0-input-prompt-BasePromptTemplate",
            type: "buttonedge",
            id: "promptTemplate_0-promptTemplate_0-output-promptTemplate-PromptTemplate|BaseStringPromptTemplate|BasePromptTemplate|Runnable-llmChain_0-llmChain_0-input-prompt-BasePromptTemplate"
        });
    }
    return links;
  }

  const nodes = inputArray
    .map(item => item.toLowerCase().replace(/\s+/g, ''))
    .filter(key => nodeMappings[key])
    .map(key => nodeMappings[key]);

  const outputJson = {
    "description": "A testing demo for JHU-specific components",
    "badge": "NEW",
    "nodes": nodes,
    "edges": linkComponents(inputArray)
  };

  fs.writeFile('output.json', JSON.stringify(outputJson, null, 2), 'utf8', (err) => {
    if (err) {
      console.log("An error occurred while writing JSON Object to File.");
      return console.log(err);
    }
    console.log("JSON file has been saved.");
  });
}

// Example usage
const input = [
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
];

const extractNames = (components) => {
  return components.map(component => {
      var [name] = component.name.split('@');
      if(name == "HTTP_API_Get"){
        name = "HTTPGET";
      }
      if(name == "HTTP_API_Post"){
        name = "HTTPPost";
      }
      if(name == "OpenAIAgents"){
        name = "openai";
      }
      if(name == "PromptBuilder"){
        name = "prompttemplate";
      }
      return name;
  });
};
let curr = extractNames(input);
if( curr.includes('openai') && curr.includes('prompttemplate')){
  curr.push("llmchain")
}
console.log(curr)
generateJson(curr);
