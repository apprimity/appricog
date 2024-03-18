from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class Response(BaseModel):
    """Final response to the question being asked"""

    output: str = Field(description="The final output to respond to the user")
    sources: List[int] = Field(
        description="List of page chunks that contain answer to the question. Only include a page chunk if it contains relevant information"
    )
