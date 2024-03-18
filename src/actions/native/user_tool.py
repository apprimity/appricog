from langchain_community.tools import Tool
from actions.semantic.base_semantic_action import default_handle_tool_error
from services.login_services import fake_decode_token


def fetch_user_details(username):
    user = fake_decode_token(username)
    return user.model_dump_json()


user_details_tool = Tool(
    name="User Details Tool",
    func=fetch_user_details,
    description="""
 This tool returns user details like name, gender, email and so on based on the provided username. 
 """,
    handle_tool_error=default_handle_tool_error,
)
