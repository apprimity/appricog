from langchain.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools import Tool

from models.query import Query
from actions.semantic.base_semantic_action import default_handle_tool_error

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

wikipedia_search_tool = Tool(
    name=wikipedia.name,
    func=wikipedia.run,
    description=wikipedia.description,
    # args_schema=Query,
    handle_tool_error=default_handle_tool_error,
)
