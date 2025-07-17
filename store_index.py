from src.helper import load_pdf, text_split, download_hugging_face_embeddings
# from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
# import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

print(f"PINECONE_API_KEY: {PINECONE_API_KEY}")
print(f"PINECONE_ENVIRONMENT: {PINECONE_API_ENV}")


extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

# Create index if it doesn't exist
index_name = "testing"

vectorstore_from_docs = PineconeVectorStore.from_documents(
        text_chunks,
        index_name=index_name,
        embedding=embeddings
    )
