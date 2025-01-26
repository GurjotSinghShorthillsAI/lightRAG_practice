import os
import logging
import asyncio
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langsmith import traceable
from sentence_transformers import SentenceTransformer

from openai import AzureOpenAI
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from langchain.prompts import PromptTemplate
from transaction_logger import mylogger

# Configure Logging
logging.basicConfig(level=logging.DEBUG)

class TransactionProcessor:
    """
    Class to process transactions using LightRAG and Azure OpenAI.
    It reads data, splits it into chunks, queries the model, and logs the results.
    """

    def __init__(self, pdf_path, excel_path, working_dir):
        # Load environment variables
        load_dotenv()
        self.azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        # File paths and working directory
        self.pdf_path = pdf_path
        self.excel_path = excel_path
        self.working_dir = working_dir

        # Initialize global token trackers
        self.total_input_tokens = 0
        self.total_output_tokens = 0

        # Initialize LightRAG instance
        self.rag = None

    @traceable
    async def llm_model_func(self, prompt, system_prompt=None, history_messages=[], **kwargs):
        """
        Azure OpenAI chat function to interpret transactions using prompts.
        """
        # Create AzureOpenAI client
        client = AzureOpenAI(
            api_key=self.azure_openai_api_key,
            api_version=self.azure_openai_api_version,
            azure_endpoint=self.azure_openai_endpoint,
        )

        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})

        # Call Azure OpenAI API
        chat_completion = client.chat.completions.create(
            model=self.azure_openai_deployment,
            messages=messages,
            temperature=kwargs.get("temperature", 0),
            top_p=kwargs.get("top_p", 1),
            n=kwargs.get("n", 1),
        )

        # Track tokens
        usage = chat_completion.usage
        self.total_input_tokens += usage.prompt_tokens
        self.total_output_tokens += usage.completion_tokens

        # Return content
        return chat_completion.choices[0].message.content

    @traceable
    async def embedding_func(self, texts: list[str]) -> np.ndarray:
        """
        Generate embeddings for the provided texts using SentenceTransformer.
        """
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings

    def configure_rag(self):
        """
        Configures the LightRAG instance with the LLM model and embedding function.
        """
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)

        self.rag = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=self.llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=384,
                max_token_size=8192,
                func=self.embedding_func,
            ),
        )

        # Insert PDF content if applicable
        if os.path.exists(self.pdf_path):
            with open(self.pdf_path, "r") as file:
                text = file.read()

            # Split text into chunks
            chunks = text.split('///')
            chunks = [chunk.strip() for chunk in chunks]

            # Insert chunks into LightRAG
            self.rag.insert_custom_chunks(text, chunks)

    def process_excel(self):
        """
        Load and process the Excel file to extract transactions.
        """
        data = pd.read_excel(self.excel_path)
        columns_to_extract = [
            'Sr No',
            'PO Line Item Description',
            'Line Description',
            'Expense GL Description',
            'Invoice Description',
            'Section as required in TDS Return'
        ]
        return data[columns_to_extract]

    def process_transaction(self, transaction):
        """
        Process a single transaction and query LightRAG in hybrid mode.
        """
        # Create prompt
        # prompt = PromptTemplate(
        #     input_variables=["po_desc", "line_desc", "gl_desc", "invoice_desc"],
        #     template="""
        #     Can you help me interpret this transaction in a single line? Return only the single line interpretation and nothing else.
        #     Transaction Details: {{
        #         "po_desc": "{po_desc}",
        #         "line_desc": "{line_desc}",
        #         "gl_desc": "{gl_desc}",
        #         "invoice_desc": "{invoice_desc}"
        #     }}
        #     """
        # )
        prompt = PromptTemplate(
            input_variables=["po_desc", "line_desc", "gl_desc", "invoice_desc"],
            template="""
            You are provided with details of a transaction including descriptions from various fields. Using the descriptions given below, generate a concise yet comprehensive summary that captures all essential aspects of the transaction.

            Transaction Details: {{
                "po_desc": "{po_desc}",
                "line_desc": "{line_desc}",
                "gl_desc": "{gl_desc}",
                "invoice_desc": "{invoice_desc}"
            }}

            Please provide a summary that integrates information from all the above fields to offer a complete understanding of the transaction in one or two sentences.
            """
        ).format(
            po_desc=transaction["PO Line Item Description"],
            line_desc=transaction["Line Description"],
            gl_desc=transaction["Expense GL Description"],
            invoice_desc=transaction["Invoice Description"],
        )

        # Get summary from LLM
        summary = asyncio.run(self.llm_model_func(prompt))

        # Query in hybrid mode
        hybrid_response = self.rag.query_with_keywords(
            summary=summary,
            param=QueryParam(mode="hybrid", top_k=5, transaction_no=transaction['Sr No'])
        )

        mylogger.update_transaction(transaction['Sr No'], "hybrid", **{
            "Retrieved Section": hybrid_response,
            "Original Answer": transaction["Section as required in TDS Return"],
            "Transaction summary": summary
        })

    def interpret_transactions(self):
        """
        Process all transactions and output results.
        """
        transactions = self.process_excel()

        for _, transaction in transactions.iterrows():
            self.process_transaction(transaction)

        mylogger.save_to_excel()

    def run(self):
        """
        Main pipeline to configure RAG, process transactions, and log token usage.
        """
        self.configure_rag()
        self.interpret_transactions()

        # Log token usage
        print("########################## Token Usage #####################################")
        print("Total Input Tokens:", self.total_input_tokens)
        print("Total Output Tokens:", self.total_output_tokens)


if __name__ == "__main__":
    pdf_path = "final_docs.txt"
    excel_path = "sample_wht_100_data.xlsx"
    working_dir = "./final_database"

    processor = TransactionProcessor(pdf_path, excel_path, working_dir)
    processor.run()
