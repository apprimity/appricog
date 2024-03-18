from langchain_community.tools import Tool
from langchain_community.utilities.serpapi import SerpAPIWrapper

from models.query import Query
from actions.semantic.base_semantic_action import default_handle_tool_error

search = SerpAPIWrapper()
online_search_tool = Tool(
    name="Online Search",
    func=search.run,
    description="""Use this tool to gather details about following:
              1. current events, OR
              2. the current state of the world, OR
              3. if you need to find relevant details from the Internet or other Online stores
              """,
    # args_schema=Query,
    handle_tool_error=default_handle_tool_error,
)
