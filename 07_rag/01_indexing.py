from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()
# import getpass
# import os
# GOOGLE_API_KEY = "AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ"

# if not os.getenv("GOOGLE_API_KEY"):
#     os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

pdf_path = Path(__file__).parent / "Leave Policy - 2026.pdf"

#Loading the file in the python program 

loader = PyPDFLoader(file_path=pdf_path)

docs= loader.load()

# print(docs[1])

# Split the docs into smaller chunks

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

chunks = text_splitter.split_documents(documents=docs)

embedding_model = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

vector_store = QdrantVectorStore.from_documents(documents=chunks,
                                                embedding=embedding_model,
                                                url = "http://localhost:6333",
                                                collection_name = "HighBrow Leave Policy") 




print("Indexing of document is done... ")