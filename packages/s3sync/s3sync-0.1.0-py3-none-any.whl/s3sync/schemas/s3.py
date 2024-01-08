from pydantic import BaseModel, Field


class S3Config(BaseModel):
    bucket_name: str = Field(min_length=1)
    region_name: str = Field(min_length=1)
    access_key_id: str = Field(min_length=1)
    secret_access_key: str = Field(min_length=1)
