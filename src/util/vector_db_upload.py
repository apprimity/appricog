from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.llms.openai import AzureOpenAI
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from util.common import env, embedding_model, logger
import os


def refresh_knowledge_base() -> list:
    # Set knowledge base directory
    result = list()
    directory = "knowledge_data"
    vector_db = None
    persist_directory = os.path.join("knowledge_base", "data")
    embeddings = embedding_model

    # Iterate over files in above directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        # Check if it is a file
        if os.path.isfile(f):
            # PDF Loader
            if f.endswith(".pdf"):
                loader = PyPDFLoader(f)
                docs = loader.load_and_split()
                logger.info("embedded", f)
            elif f.endswith(".txt"):  # Text Loader
                loader = TextLoader(f, encoding="utf-8")
                docs = loader.load_and_split()
                logger.info("embedded", f)
            try:
                # Initialize Chroma VectorDB or add documents as needed
                if not vector_db:
                    vector_db = Chroma.from_documents(
                        documents=docs,
                        embedding=embeddings,
                        persist_directory=persist_directory,
                    )
                    # Persist vector DB
                    vector_db.persist()
                else:
                    vector_db.add_documents(docs)
                result.append(f + " --> Vectorization Status " + "Success")
            except Exception as e:
                result.append(f + " --> Vectorization Status " + "Error")

    return result
