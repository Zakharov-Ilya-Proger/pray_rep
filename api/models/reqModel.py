from pydantic import BaseModel, Field


class reqModel(BaseModel):
    id: str = Field(
        ...,
        description='''Room id, to load audio''',
        examples=['КИКАЕТАЦИФАРАКИ']
    )
    api_pass: str = Field(
        ...,
        description='''Password for working with the API''',
        examples=['КИКАЕТАБУКАВАКИ']
    )
