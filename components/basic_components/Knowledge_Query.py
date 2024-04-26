import json
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from components.base_component import BaseComponent
# import faiss
import numpy as np


class KnowledgeQueryComponent(BaseComponent):
    builder_description = r"""
    This component acts as a bridge between natural language queries and a corpus of knowledge. It takes in a textual query and a body of knowledge data, then utilizes OpenAI's embedding capabilities to understand and extract the most relevant pieces of information from the knowledge data. The component requires three key inputs:
    1. 'query': A string representing the user's query.
    2. 'knowledge_data': A lengthy string containing the text data to be searched. This data should be a large collection that contains some useful information sparsely.
    3. 'k': The number of top relevant results the component should return. This is crucial for tailoring the depth of information retrieval to the user's needs.
    The output, 'retrieved_documents', is a detailed JSON string encapsulating the most relevant findings, making it easy to integrate and use in downstream components.
    """

    thinker_description = r"""
    The KnowledgeQueryComponent is designed for scenarios where understanding and extracting specific information from a larger body of text is necessary. It's particularly useful in workflows that involve dynamic data analysis, content summarization, or information retrieval tasks based on user queries. To integrate this component, ensure that the knowledge data is connected to a large volume data and that the query shows some keywords. This component should be placed after any data source (e.g. DocumentLoader) and before any components that require the extracted information for further processing (e.g. OpenAIAgent).
    """

    component_schema = r"""
    {
        "name": "KnowledgeQuery",
        "description": "Queries knowledge data using a natural language query to find the most relevant information.",
        "inputs": [
            {
                "parameter": "query",
                "description": "The query string used to search the knowledge data, expressed in natural language.",
                "type": "string",
                "example": "Explain the theory of relativity"
            },
            {
                "parameter": "knowledge_data",
                "description": "The string containing the corpus of knowledge data. This should include comprehensive information related to the query's context.",
                "type": "string",
                "example": "In physics, the theory of relativity, or simply relativity, encompasses two theories by Albert Einstein..."
            },
            {
                "parameter": "k",
                "description": "Specifies the number of top results to retrieve, as a string.",
                "type": "string",
                "example": "3"
            }
        ],
        "outputs": [
            {
                "parameter": "retrieved_documents",
                "description": "A JSON string containing the top k relevant pieces of information extracted from the knowledge data, including their relevance scores.",
                "type": "string",
                "example": "{\"documents\": [{\"id\": 1, \"text\": \"Einstein's theory of relativity is...\", \"score\": 0.98}, {\"id\": 2, \"text\": \"General relativity is a theory of gravitation...\"]}"
            }
        ]
    }
    """

    def __init__(self, component_id, query, knowledge_data, k, openai_api_key, **vars):
        super().__init__(component_id)
        self.query = query
        self.knowledge_data = knowledge_data
        self.k = k
        self.openai_api_key = openai_api_key


    def execute(self, inputs, user_params=None):
        openai.api_key = self.openai_api_key
        Chroma_vs = self._initialize_chroma_vectorstore(inputs)

        # # Embed the query
        # response = openai.Embedding.create(
        #     input=inputs['query'],
        #     model="text-embedding-ada-002"
        # )
        #
        # query_embedding = response['data'][0]['embedding']

        # Retrieve relevant documents based on the query embedding
        retrieved_docs = Chroma_vs.similarity_search(inputs['query'])
        retrived_content = ""
        for doc in retrieved_docs:
            retrived_content += doc.page_content

        # Assuming `retrieved_docs` is a list of dictionaries, each containing 'id', 'text', and 'score'
        self.output = json.dumps({"documents": retrived_content })
        self.is_output_fresh = True


    def _initialize_chroma_vectorstore(self,inputs):
        # Manually prepare the documents from the input string
        docs = [{"id": 0, "text": inputs['knowledge_data']}]

        # Split documents into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                       chunk_overlap=200)  # TODO hard coded here, can be change to something dynamic/input.
        # splits = text_splitter.split_documents(docs)
        splits = text_splitter.split_text(inputs['knowledge_data'])

        # Use OpenAIEmbeddings to embed documents
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)

        # Create a Chroma vector store from the embedded documents
        # vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        vectorstore = Chroma.from_texts(texts=splits, embedding=embeddings)
        # retriever = vectorstore.as_retriever()
        return vectorstore
