from pydantic import BaseModel, Field


class reqModel(BaseModel):
    id: str = Field(
        ...,
        description='''Room id, to load audio''',
        examples=['КИКАЕТАЦИФАРАКИ']
    )
