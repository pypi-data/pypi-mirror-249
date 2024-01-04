from pydantic import BaseModel, validator
from ..request.cep import Cep
from typing import Optional


class Endereco(BaseModel):
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None
    referencia: Optional[str] = None

    @validator("cep")
    def validate_cep(cls, value):
        response = Cep(version=1).get(value)
        return response.cep
