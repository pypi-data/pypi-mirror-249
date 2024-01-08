from pydantic import BaseModel, Field


class LocalConfig(BaseModel):
    path: str = Field(min_length=1)
