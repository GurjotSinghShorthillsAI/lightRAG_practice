import os
import logging
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langsmith import traceable
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# LightRAG imports
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc

# OpenAI / Azure OpenAI
import numpy as np
from openai import AzureOpenAI


logging.basicConfig(level=logging.DEBUG)
load_dotenv()


class PDFChatbotRAG:
    """
    An object-oriented class that:
      1. Loads PDF files and extracts text.
      2. Splits text into chunks.
      3. Creates a LightRAG instance for query-based retrieval and summarization.
      4. Uses Azure OpenAI for the LLM calls.
      5. Uses SentenceTransformers for text embeddings.
      6. Allows an interactive loop to query the RAG system.
    """

    def __init__(
        self,
        pdf_directory: str = "test_files",
        working_directory: str = "./test_output",
        azure_openai_deployment: str = None,
        azure_openai_api_key: str = None,
        azure_openai_endpoint: str = None,
        azure_openai_api_version: str = None,
    ):
        """
        Initializes the PDFChatbotRAG with directory paths and Azure/OpenAI credentials.

        Args:
            pdf_directory (str): The folder path where PDF files are located.
            working_directory (str): Folder path for LightRAG’s working directory.
            azure_openai_deployment (str): The deployment name of the Azure OpenAI model.
            azure_openai_api_key (str): The API key for Azure OpenAI.
            azure_openai_endpoint (str): The endpoint URL for Azure OpenAI.
            azure_openai_api_version (str): The API version for Azure OpenAI.
        """
        self.pdf_directory = pdf_directory
        self.working_directory = working_directory

        # Load environment variables if not explicitly provided
        self.azure_openai_deployment = azure_openai_deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.azure_openai_api_key = azure_openai_api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = azure_openai_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_version = azure_openai_api_version or os.getenv("AZURE_OPENAI_API_VERSION")

        # Tracking tokens usage across the entire session
        self.total_input_tokens = 0
        self.total_output_tokens = 0

        # Will be assigned after text extraction
        self.text = ""
        self.text_chunks = []

        # The final LightRAG instance
        self.rag = None

        # Create working directory if not exists
        if not os.path.exists(self.working_directory):
            os.mkdir(self.working_directory)

    def load_pdfs(self):
        """
        Reads all PDFs in the specified directory (self.pdf_directory),
        extracts text from each page, and appends it to self.text.
        """
        for pdf_file in os.listdir(self.pdf_directory):
            # Only process .pdf files
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(self.pdf_directory, pdf_file)
                reader = PdfReader(pdf_path)

                # Extract text from each page
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        self.text += page_text + "\n"

                print(f"Processed {pdf_file}")

    @traceable
    async def _llm_model_func(
        self,
        prompt: str,
        system_prompt: str = None,
        history_messages=None,
        keyword_extraction: bool = False,
        **kwargs
    ) -> str:
        """
        Azure OpenAI chat function for the LLM calls.
        This function is used by LightRAG for generating or summarizing text
        based on the retrieved context.

        Args:
            prompt (str): The user's question or the text prompt.
            system_prompt (str): The system-level instructions (optional).
            history_messages (list): Conversation history to pass to the model (optional).
            keyword_extraction (bool): Whether to process prompt for keywords (LightRAG usage).
            kwargs: Additional parameters for controlling LLM behavior (temperature, top_p, etc.)

        Returns:
            str: The model's textual response.
        """
        if history_messages is None:
            history_messages = []

        # Create AzureOpenAI client
        client = AzureOpenAI(
            api_key=self.azure_openai_api_key,
            api_version=self.azure_openai_api_version,
            azure_endpoint=self.azure_openai_endpoint,
        )

        # Build the prompt messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})

        print("Raw Message to LLM:")
        print(messages)

        # Call the Azure OpenAI Chat Completions
        chat_completion = client.chat.completions.create(
            model=self.azure_openai_deployment,
            messages=messages,
            temperature=kwargs.get("temperature", 0),
            top_p=kwargs.get("top_p", 1),
            n=kwargs.get("n", 1),
        )

        print("Raw Response from LLM:")
        print(chat_completion)

        # Update token usage statistics
        prompt_tokens = chat_completion.usage.prompt_tokens
        completion_tokens = chat_completion.usage.completion_tokens
        total_tokens = chat_completion.usage.total_tokens

        print(f"Prompt Tokens: {prompt_tokens}")
        print(f"Completion Tokens: {completion_tokens}")
        print(f"Total Tokens Used: {total_tokens}")

        self.total_input_tokens += prompt_tokens
        self.total_output_tokens += completion_tokens

        return chat_completion.choices[0].message.content

    @traceable
    async def _embedding_func(self, texts: list[str]) -> np.ndarray:
        """
        Provides embeddings for a list of texts using SentenceTransformer.
        This is the function LightRAG calls to embed both queries and documents.
        """
        model = SentenceTransformer("all-MiniLM-L6-v2")

        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings

    def initialize_rag(self):
        """
        Creates and configures the LightRAG instance using:
          - self._llm_model_func as the LLM.
          - self._embedding_func as the embedding function.
          - The working directory for indexing and caching.
        """
        self.rag = LightRAG(
            working_dir=self.working_directory,
            llm_model_func=self._llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=384,
                max_token_size=8192,
                func=self._embedding_func,
            ),
        )
        self.rag.insert(self.text)

    def chat_loop(self):
        """
        The main interactive loop to query the RAG system.
        Type 'exit' to quit the loop.
        Prints the final answer from the RAG system.
        """
        while True:
            print("Total input tokens:", self.total_input_tokens)
            print("Total output tokens:", self.total_output_tokens)
            print("Total tokens used:", self.total_input_tokens + self.total_output_tokens)

            question = input("Enter your question (type 'exit' to quit): ")

            if question.lower() == "exit":
                print("Exiting the chatbot. Goodbye!")
                break

            # Perform query using LightRAG
            response = self.rag.query(
                question, 
                param=QueryParam(mode="hybrid", top_k=5, response_type="Single line")
            )

            print(f"Answer: {response}\n")

    def run(self):
        """
        Convenience method to run the entire pipeline:
         1. Load PDF files and extract text.
         2. Initialize LightRAG instance.
         3. Start interactive chat loop.
        """
        # 1) Load PDFs
        self.load_pdfs()

        # 2) Initialize RAG
        self.initialize_rag()

        # 3) Start Chat Loop
        self.chat_loop()

if __name__ == "__main__":
    # Create an instance with default paths/env
    chatbot = PDFChatbotRAG(
        pdf_directory="test_files",
        working_directory="./test_output_custom_insert",
    )
    # Run the full pipeline
    chatbot.run()