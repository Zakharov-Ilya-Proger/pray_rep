from pydantic import BaseModel


class reqModel(BaseModel):
    id: str
    api_pass: str
