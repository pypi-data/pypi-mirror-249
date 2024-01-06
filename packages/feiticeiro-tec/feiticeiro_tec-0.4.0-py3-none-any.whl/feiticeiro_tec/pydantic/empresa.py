from pydantic import BaseModel, validator
from .endereco import Endereco
from .contato import Contato
from ..validate import Cnpj


class EmpresaBase:
    cnpj: str
    razao_social: str
    nome_fantasia: str
    endereco: Endereco
    contato: Contato

    @validator("cnpj")
    def validate_cnpj(cls, value):
        cnpj = Cnpj()
        cnpj.validate(value)
        return cnpj.mask(value)


class Empresa(EmpresaBase, BaseModel):
    ...


class EmpresaContatoOptional(EmpresaBase, BaseModel):
    contato: Contato = None
