import os

# Environment variables
neo4j_url = os.environ.get("NEO4J_URL")
neo4j_user = os.environ.get("NEO4J_USER")
neo4j_password = os.environ.get("NEO4J_PASS")
local_model_name = os.environ.get("LOCAL_MODEL_NAME", "")
use_local_model = os.environ.get("USE_LOCAL_MODEL", "false")
deployment_type = os.environ.get("DEPLOYMENT_TYPE", "")
deployment_name = os.environ.get("DEPLOYMENT_NAME", "google/flan-t5-xxl")
base_url_prefix = os.environ.get("BASE_URL_PREFIX", "")
server_host_address = os.environ.get("SERVER_HOST_ADDRESS", "")
env_config = os.environ.get("ENV_CONFIG", "")
vector_db_url = os.environ.get("VECTOR_DB_URL")
vector_db_user = os.environ.get("VECTOR_USER", "")
vector_db_password = os.environ.get("VECTOR_PASS", "")
vector_search_collection_name = os.environ.get("VECTOR_SEARCH_COLLECTION_NAME", "")
vector_db_enabled = os.environ.get("VECTOR_DB_ENABLED", "")
max_token_limit = os.environ.get("MAX_TOKEN_LIMIT", "300")
max_execution_time = os.environ.get("MAX_EXECUTION_TIME", "5")
early_stopping_enabled = os.environ.get("EARLY_STOPPING_ENABLED", "false")
cypher_return_limit = os.environ.get("CYPHER_RETURN_LIMIT", "")
app_title = os.environ.get("APP_TITLE", "LLM Framework")
debug_enabled = os.environ.get("DEBUG", "false")

# Variables derived from environment variables
is_prod = True if env_config.lower() == "prod" else False
is_vector_db_enabled = True if vector_db_enabled.lower() == "true" else False
is_early_stopping_enabled = True if early_stopping_enabled.lower() == "true" else False
is_cypher_return_limit_enabled = True if cypher_return_limit != "" else False
is_local_model = True if use_local_model.lower() == "true" else False
is_debug = True if debug_enabled.lower() == "true" else False
chroma_db_file = os.getenv("VECTOR_STORE", os.path.join("knowledge_base", "data"))
cypher_limit_query = (
    (" limit " + cypher_return_limit) if is_cypher_return_limit_enabled else ""
)
