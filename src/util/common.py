from typing import List, Optional, Tuple, Dict

# from langchain_community.graphs import Neo4jGraph
import util.environment as env
from langchain_community.embeddings import (
    AzureOpenAIEmbeddings,
    OpenAIEmbeddings,
    HuggingFaceEmbeddings,
    OllamaEmbeddings,
)
from fastapi import Request
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
)
from util.logger import logger

# Initialize Graph Database as needed
# try:
#     graph_database = Neo4jGraph(
#         url=env.neo4j_url, username=env.neo4j_user, password=env.neo4j_password
#     )
# except Exception:
#     graph_database = None

# Initialize Embedding model
embedding_model = (
    OllamaEmbeddings(model=env.local_model_name)
    if env.is_local_model
    else (
        HuggingFaceEmbeddings()
        if env.deployment_type.lower() == "huggingface"
        else (
            AzureOpenAIEmbeddings(chunk_size=1)
            if env.deployment_type.lower() == "azure"
            else None
        )
    )
)

# Fake users DB
# TODO: Need to replace this with a proper OAuth 2.0 based security module
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_basic = HTTPBasic()

__version__ = "0.1.0"
