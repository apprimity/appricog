import contextlib
import io
from typing import Dict
from inference_engines.knowledge_base_engine import KnowledgeBaseEngine
from langchain.callbacks.streaming_aiter_final_only import (
    AsyncFinalIteratorCallbackHandler,
)
from util.environment import deployment_name

from util.logger import logger

# Initialize base engine required for the services
engine = KnowledgeBaseEngine()
agent_chain = engine.initialize(deployment_name=deployment_name)


def get_response_and_thought(message: str, current_user):
    """Get response and thought from extracted json"""

    response, thought = execute_chain_from_engine(message, current_user)
    return {"response": response, "thought": thought}


def execute_chain_from_engine(message, current_user=None):
    """Execute agent chain from the pre-initialized base engine"""
    response = ""

    # Append current user name to the message
    if current_user is not None:
        message = "Username: " + current_user.username + "\n" + message

    try:
        if hasattr(agent_chain, "verbose"):
            agent_chain.verbose = True
        chat_input = None
        memory_key = ""
        logger.info("Memory ID:")
        logger.info(agent_chain.memory.__dir__)

        if hasattr(agent_chain, "memory") and agent_chain.memory is not None:
            memory_key = agent_chain.memory.memory_key

        for key in engine.input_keys:
            if key not in [memory_key, "chat_history"]:
                chat_input = {key: message}

        with io.StringIO() as output_buffer, contextlib.redirect_stdout(output_buffer):
            try:
                response = agent_chain.invoke(chat_input)
            except Exception as exc:
                # make the error message more informative
                logger.debug(f"Error: {str(exc)}")
                # output = agent_chain.run(chat_input)

            thought = output_buffer.getvalue().strip()
            logger.info(thought)

    except Exception as exc:
        # raise ValueError(f"Error: {str(exc)}") from exc
        raise exc

    return response, thought


def get_response(message: str, current_user):
    """Get response from extracted json"""
    response, thought = execute_chain_from_engine(message, current_user)

    # Return the response as-is if a string
    if isinstance(response, str):
        return {"response": response}

    # Return the output portion from response
    return {"response": response["output"]}


# TODO: Fix the code below
def stream_chains(message, current_user=None):
    """Stream response from extracted json"""
    response = ""

    # Append current user name to the message
    if current_user is not None:
        message = "Username: " + current_user.username + "\n" + message

    try:
        if hasattr(agent_chain, "verbose"):
            agent_chain.verbose = True
        chat_input = None
        memory_key = ""
        logger.info("Memory ID:")
        logger.info(agent_chain.memory.__dir__)

        if hasattr(agent_chain, "memory") and agent_chain.memory is not None:
            memory_key = agent_chain.memory.memory_key

        for key in agent_chain.input_keys:
            if key not in [memory_key, "chat_history"]:
                chat_input = {key: message}

        # Create the callback handler
        callback_handler = AsyncFinalIteratorCallbackHandler()

        with io.StringIO() as output_buffer, contextlib.redirect_stdout(output_buffer):
            try:
                for chunk in agent_chain.stream(
                    chat_input,  # callbacks=[callback_handler]
                ):
                    yield chunk["output"]

            except Exception as exc:
                # make the error message more informative
                logger.debug(f"Error: {str(exc)}")
                # output = knowledge_graph_agent.run(chat_input)

            thought = output_buffer.getvalue().strip()
            logger.info(thought)

    except Exception as exc:
        # raise ValueError(f"Error: {str(exc)}") from exc
        raise exc
