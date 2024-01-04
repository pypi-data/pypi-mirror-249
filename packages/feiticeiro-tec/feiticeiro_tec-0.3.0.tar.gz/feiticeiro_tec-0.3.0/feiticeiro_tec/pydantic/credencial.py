from pydantic import BaseModel


class CredencialEmail(BaseModel):
    email: str
    senha: str


class CredencialUsername(BaseModel):
    username: str
    senha: str


class CredencialCnpj(BaseModel):
    cnpj: str
    senha: str


class CredencialCpf(BaseModel):
    cpf: str
    senha: str


class CredencialLogin(BaseModel):
    login: str
    senha: str
