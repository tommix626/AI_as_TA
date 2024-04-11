import fitz  # PyMuPDF
import docx
from components.base_component import BaseComponent
import json

class DocumentLoaderComponent(BaseComponent):
    thinker_description = r"""
        The DocumentLoaderComponent serves as a versatile tool for retrieving textual data from various document formats. Its primary role is to abstract away the complexities of reading different file types, allowing users to focus on the content's analysis or processing rather than on the nuances of file handling. Whether dealing with academic papers in PDF format or reports in DOC format, this component ensures that the content becomes readily accessible in a uniform string format for further manipulation or examination. 
               """

    builder_description = r"""This component is essential for workflows that begin with extracting text from documents. Given a file path, it intelligently determines the file type and employs the appropriate library to extract the document's content. The DocumentLoaderComponent is particularly useful in preprocessing pipelines, where initial data collection involves gathering information from documents of various formats. Integration into such pipelines enables seamless content extraction, setting the stage for subsequent analysis, such as natural language processing or data categorization tasks."""

    component_schema = r"""
    {
  "name": "DocumentLoader",
  "description": "Loads and extracts text content from documents of various formats, including PDF and DOC, returning the content as a string.",
  "inputs": [
    {
      "parameter": "resource_path",
      "description": "The file path to the document from which content is to be extracted. The component supports multiple formats and determines the appropriate method for extraction based on the file extension. Start your path with ./resource and specify an arbitrary name that is suitable. The document will be ",
      "type": "string",
      "example": "./resource/document.pdf"
    }
  ],
  "outputs": [
    {
      "parameter": "document_content",
      "description": "The extracted text content from the document. In cases where the document contains non-text elements (images, tables, etc.), only the textual components are returned, and non-text elements are ignored or appropriately handled depending on their nature and the capabilities of the extraction library used.",
      "type": "string",
      "example": "This is the content of the document..."
    }
  ]
}
"""
    def __init__(self, component_id, resource_path, **kwargs):
        super().__init__(component_id)
        self.resource_path = resource_path

    def prepare_inputs(self):
        inputs = {}

        inputs['resource_path'] = self.resource_path() if callable(self.resource_path) else self.resource_path
        # Ensure the resource path is a string
        if not isinstance(self.resource_path, str):
            raise TypeError("resource_path should be a string.")


    def execute(self, inputs):
        # Determine the file type and choose the appropriate loader
        if inputs['resource_path'].endswith('.pdf'):
            self.output = self._load_pdf_content(inputs['resource_path'])
        elif inputs['resource_path'].endswith('.docx'):
            self.output = self._load_docx_content(inputs['resource_path'])
        else:
            raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")
        self.is_output_fresh = True

    def get_output(self):
        if not self.is_output_fresh:
            self.run()
        return self.output

    def _load_pdf_content(self, path):
        # Load and extract text from a PDF file
        content = []
        with fitz.open(path) as doc:
            for page in doc:
                content.append(page.get_text())
        return '\n'.join(content)

    def _load_docx_content(self, path):
        # Load and extract text from a DOCX file
        doc = docx.Document(path)
        content = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(content)

