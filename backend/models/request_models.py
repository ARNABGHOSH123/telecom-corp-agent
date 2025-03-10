from pydantic import BaseModel, Field


class ErrorQuery(BaseModel):
    query: str = Field(description="The full error query from the user")
