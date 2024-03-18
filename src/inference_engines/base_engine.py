from typing import Any, Union
from langchain.agents import AgentExecutor, BaseSingleActionAgent, BaseMultiActionAgent
from langchain.agents.tools import Tool
from langchain_community.chat_models.azure_openai import ChatOpenAI, AzureChatOpenAI
from langchain_community.llms.openai import AzureOpenAI
from langchain.memory import ConversationBufferWindowMemory, ReadOnlySharedMemory
from langchain_core.memory import BaseMemory
from langchain_community.chat_models.azure_openai import ChatOpenAI, AzureChatOpenAI
from langchain_community.llms.openai import AzureOpenAI
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.llms.ollama import Ollama
from langchain_community.chat_models.ollama import ChatOllama
from util.common import env
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.globals import set_debug

set_debug(env.is_debug)

CHAT_SUFFIX = """Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}"""

DEFAULT_CHAT_AGENT_SYSTEM_MSG = """
Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
"""

DEFAULT_CHAT_AGENT_HUMAN_MSG = """
{input}

{agent_scratchpad}
 (reminder to respond in a JSON blob no matter what)
"""

DEFAULT_CHAT_AGENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", DEFAULT_CHAT_AGENT_SYSTEM_MSG),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", DEFAULT_CHAT_AGENT_HUMAN_MSG),
    ]
)


class BaseEngine:
    """Base Engine class to interact with Agent Executors"""

    # Fields
    agent_chain: AgentExecutor
    verbose: Any
    memory: BaseMemory
    tools: list[Tool]
    input_keys: list[str]
    llm: Any

    def init_llm(self):
        # Initialize required LLM
        if env.deployment_type.lower() == "azure" and env.deployment_name in [
            "davinci2",
            "DavinciTest",
            "davinciCode",
            "gpt35",
        ]:
            llm = AzureOpenAI(deployment_name=env.deployment_name, temperature=0)
        elif env.deployment_type.lower() == "azure" and env.deployment_name.lower() in [
            "gpt-4"
        ]:
            llm = AzureChatOpenAI(deployment_name=env.deployment_name, temperature=0)
        elif env.is_local_model:

            # Ollama
            llm = ChatOllama(model=env.local_model_name)

            # TODO: Local Hugging face model; not workable on CPU
            # tokenizer = AutoTokenizer.from_pretrained(env.local_model_path)
            # model = AutoModelForCausalLM.from_pretrained(env.local_model_path)
            # llm = HuggingFacePipeline.from_model_id(
            #     model_id=model,
            #     task="text-generation",
            #     device=0,
            #     model_kwargs={"temperature": 0.3, "max_new_tokens": 3000},
            # )

        elif (
            env.deployment_type.lower() == "huggingface"
            and env.deployment_name.lower()
            in [
                "google/flan-t5-xxl",
                "huggingfaceh4/zephyr-7b-alpha",
                "huggingfaceh4/zephyr-7b-beta",
                "mistralai/mixtral-8x7b-instruct-v0.1",
            ]
        ):

            llm = HuggingFaceEndpoint(
                repo_id=env.deployment_name,
                max_new_tokens=3000,
                temperature=0.3,
            )

        else:
            raise Exception(
                f"Deployment model {env.deployment_name} is currently not supported"
            )

        # Assign the new llm
        self.llm = llm

    @staticmethod
    def function_name():
        return "BaseEngine"

    def initialize(
        self, agent: Union[BaseSingleActionAgent, BaseMultiActionAgent], *args, **kwargs
    ):
        """Method to initialize Agent Chain"""
        self.agent_chain = AgentExecutor(
            tools=self.tools,
            # llm=llm_with_stop,
            agent=agent,
            verbose=self.verbose,
            max_execution_time=(
                env.max_execution_time if env.is_early_stopping_enabled else None
            ),
            early_stopping_method="generate",
            memory=self.memory,
            handle_parsing_errors=True,
            **kwargs,
        )

        return self.agent_chain

    def __init__(self, *args, **kwargs):
        self.init_llm()
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        return self.agent_chain.run(*args, **kwargs)
