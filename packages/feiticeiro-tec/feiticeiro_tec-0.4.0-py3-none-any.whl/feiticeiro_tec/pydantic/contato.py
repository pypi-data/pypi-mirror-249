from pydantic import BaseModel, validator
from typing import Optional
from ..validate import Email


class Contato(BaseModel):
    telefone: Optional[str]
    email: Optional[str]

    @validator("email")
    def validate_email(cls, value):
        Email().validate(value)
        return value
