import os
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
import numpy as np
from dotenv import load_dotenv
import logging
from openai import AzureOpenAI
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)

load_dotenv()

AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

pdf_path = "test_files/fictional_story.pdf"

reader = PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text()

# Step 2: Configure LightRAG
WORKING_DIR = "./rag_output"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
    )

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history_messages:
        messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    chat_completion = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT, 
        messages=messages,
        temperature=kwargs.get("temperature", 0),
        top_p=kwargs.get("top_p", 1),
        n=kwargs.get("n", 1),
    )
    return chat_completion.choices[0].message.content


async def embedding_func(texts: list[str]) -> np.ndarray:

    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = model.encode(texts, convert_to_numpy=True)

    return embeddings

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=EmbeddingFunc(
        embedding_dim=384,
        max_token_size=8192,
        func=embedding_func,
    ),
    chunk_token_size= 800,
    chunk_overlap_token_size=100
)

rag.insert(text)

while True:

    question = input("Enter your question (type 'exit' to quit): ")
    
    if question.lower() == 'exit':
        print("Exiting the chatbot. Goodbye!")
        break

    # Perform query
    response = rag.query(question, param=QueryParam(mode="hybrid", top_k=5, response_type="Single word"))

    # Print the response
    print(f"Answer: {response}\n")
