from json.decoder import JSONDecodeError
from pydantic import BaseModel, Extra
from typing import Optional
from langchain.prompts.base import BasePromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.base import Chain
from langchain_core.tools import ToolException

# from langchain.agents.tools import Tool
from langchain_community.tools import Tool, StructuredTool
from langchain.memory import ConversationBufferWindowMemory, ReadOnlySharedMemory
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    format_document,
)
from langchain_core.memory import BaseMemory
from langchain.callbacks.manager import Callbacks
from typing import Dict, List, Any, Union
from abc import abstractmethod
from models.query import Query
from util.logger import logger


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def combine_output_and_docs(output: str, docs: str) -> dict:
    """Combine output and docs."""
    return {"output": output, "docs": docs}


def default_handle_tool_error(error: Exception) -> str:
    """Handles tool exceptions."""

    if isinstance(error, JSONDecodeError):
        return "Reformat in JSON and try again"
    elif error.args[0].startswith("Too many arguments to single-input tool"):
        return "Format in a SINGLE JSON STRING. DO NOT USE MULTI-ARGUMENTS INPUT."
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
        + "Please try another tool."
    )


combine_output_and_docs = RunnableLambda(combine_output_and_docs)


class BaseSemanticAction(Chain):
    """Base Semantic Action that interprets a prompt and executes python code as needed."""

    return_only_outputs: bool = False
    llm: Any

    """LLM wrapper to use."""
    llm_chain: Optional[LLMChain]
    input_key: str = "question"  #: :meta private:
    output_key: str = "answer"  #: :meta private:
    memory: Optional[BaseMemory] = None
    tool_name: str = ""
    tool_description: str = ""
    tool: Optional[Tool]
    tool_return_direct: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool = Tool(
            name=self.tool_name,
            func=self.__call__,
            description=self.tool_description,
            return_direct=self.tool_return_direct,
            args_schema=Query,
            handle_tool_error=default_handle_tool_error,
        )

    class Config:
        """Configuration for this pydantic object."""

        extra = "forbid"
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Expect input key.
        :meta private:
        """

        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Expect output key.
        :meta private:
        """
        return [self.output_key]

    def get_prompt(self, inputs: Dict[str, str]) -> BasePromptTemplate:
        """Method that gets the required prompt for a chain execution"""
        # Return a None object
        # return None

    @abstractmethod
    def chain_action(self, inputs: Dict[str, str], history=None, retry=False):
        """Method that holds the logic to be performed by chain"""

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        logger.debug(f"Base inputs for the LLM Chain: {inputs}")
        prompt = self.get_prompt(inputs=inputs)
        if prompt != None and self.llm != None:
            self.llm_chain = LLMChain(prompt=prompt, llm=self.llm)

        # Invoke the chain logic
        return self.chain_action(inputs=inputs)
