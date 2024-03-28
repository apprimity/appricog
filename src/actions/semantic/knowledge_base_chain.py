from __future__ import annotations
from operator import itemgetter
from util.common import embedding_model, env
from langchain.memory import ReadOnlySharedMemory
from langchain_core.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
)
from actions.semantic.base_semantic_action import (
    BaseSemanticAction,
    combine_documents,
)
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from chromadb.config import Settings
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from typing import Any, Dict, List, Optional
from pydantic import Field
from util.logger import logger

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)

qa_template = """
    You are a helpful AI assistant. 
    Use the provided context to answer the question at the end.   
    context: {context}
    =========
    Previous conversation history: {chat_history}
    =============
    Question: {input}
    """


class LLMKnowledgeBaseChain(BaseSemanticAction):
    """Chain for question-answering against a collection of documents in a Knowledge Base."""

    embeddings = embedding_model
    input_key = "input"
    output_key = "output"
    tool_description = """
 Function purpose:
 Purpose of this function is to find answers from the knowledge base.  
 
 Function takes the user question as its input.

 How to use:
 Function will answer the question asked by the user, by finding information from the provided context.
 Use information returned by this tool to add to the context for other tools.
 """
    tool_name = "Knowledge Base search"
    chroma_db: Optional[Chroma] = None
    qa_chain: Optional[ConversationalRetrievalChain] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch the retriever based on configured vector store
        logger.info("vector store folder: " + env.knowledge_base_dir)
        self.chroma_db = Chroma(
            persist_directory=env.knowledge_base_dir,
            embedding_function=self.embeddings,
            client_settings=Settings(
                anonymized_telemetry=False,
                # chroma_db_impl="duckdb+parquet",
                persist_directory=env.knowledge_base_dir,
                is_persistent=True,
            ),
        )
        retriever = self.chroma_db.as_retriever()  # search_kwargs={"k": 4}
        logger.info(self.chroma_db.get())

        # Use the read-only memory to prevent the tool from modifying the memory
        readonlymemory = ReadOnlySharedMemory(memory=self.memory)

        # Execute ConversationalRetrievalQA chain
        # LCEL based chain
        self.qa_chain = (
            {
                "input": RunnablePassthrough(),
                "docs": RunnablePassthrough() | retriever,
                "context": RunnablePassthrough() | retriever | combine_documents,
                "chat_history": RunnableLambda(readonlymemory.load_memory_variables)
                | itemgetter("chat_history"),
            }
            | ChatPromptTemplate.from_template(template=qa_template)
            | self.llm
        )

        # Legacy Langchain code
        # self.qa_chain = ConversationalRetrievalChain.from_llm(
        #     llm=self.llm,
        #     retriever=retriever,
        #     verbose=True,
        #     return_source_documents=True,
        #     max_tokens_limit=2000,
        #     memory=readonlymemory,
        #     combine_docs_chain_kwargs={
        #         "prompt": ChatPromptTemplate.from_template(
        #             template=qa_template,
        #             # partial_variables={"agent_scratchpad": ""},
        #         )
        #     },
        # )
        # self.qa_chain.output_key = self.output_key

    def get_prompt(self, inputs: Dict[str, str]) -> BasePromptTemplate:
        prompt = ChatPromptTemplate.from_template(
            template=qa_template,
        )
        return prompt

    def chain_action(self, inputs: Dict[str, str]):
        logger.info("Memory: ")
        logger.info(self.memory.buffer)

        logger.info("Inputs: ")
        logger.info(inputs)

        logger.info("conversational_chat created ConversationalRetrievalChain")

        response = self.qa_chain.invoke(inputs[self.input_key])
        logger.info("Response: ")
        logger.info(response)

        return {
            "input": inputs[self.input_key],
            "output": response,
        }
