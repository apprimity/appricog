from langchain_core.pydantic_v1 import BaseModel, Field


class Query(BaseModel):
    input: str = Field()
    pass
