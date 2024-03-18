from langchain.agents import create_structured_chat_agent
from langchain.memory import (
    ConversationTokenBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory,
    ReadOnlySharedMemory,
)
from parsers.response_parser import parse
from inference_engines.base_engine import BaseEngine, DEFAULT_CHAT_AGENT_PROMPT
from actions.semantic.knowledge_base_chain import LLMKnowledgeBaseChain
from actions.native.search_tool import online_search_tool
from langchain_core.output_parsers import PydanticOutputParser

from actions.native.wikipedia_tool import wikipedia_search_tool


class KnowledgeBaseEngine(BaseEngine):
    """LLM Knowledge Base Engine"""

    @staticmethod
    def function_name():
        return "KnowledgeBaseEngine"

    def initialize(self, deployment_name: str, *args, **kwargs):

        # Initialize Memory as needed
        memory = ConversationBufferWindowMemory(
            input_key="input",
            memory_key="chat_history",
            return_messages=True,
            k=2,
            output_key="output",
        )
        self.memory = memory
        self.verbose = True
        self.input_keys = [memory.input_key, memory.memory_key]

        # Tools setup for required tool configs
        self.tools = [
            wikipedia_search_tool,
            online_search_tool,
            LLMKnowledgeBaseChain(llm=self.llm, verbose=True, memory=self.memory).tool,
        ]

        # Structured Chat Agent created
        agent = create_structured_chat_agent(
            llm=self.llm, prompt=DEFAULT_CHAT_AGENT_PROMPT, tools=self.tools
        )  # | PydanticOutputParser(pydantic_object=Response) - TODO Need to fix this to get response structure returned

        # Invoke base functionality to get initialized agent chain
        return super().initialize(llm=self.llm, agent=agent, *args, **kwargs)
