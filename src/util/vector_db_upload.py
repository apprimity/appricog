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
    documents_directory = env.documents_dir
    vector_db = None
    persist_directory = env.knowledge_base_dir
    embeddings = embedding_model

    # Create the directory if it doesn't exist
    if not os.path.exists(documents_directory):
        os.makedirs(documents_directory)

    # Iterate over files in documents directory
    if os.path.isdir(documents_directory):
        for filename in os.listdir(documents_directory):
            f = os.path.join(documents_directory, filename)

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
