import re
from typing import Optional
from requests import get
from pydantic import BaseModel


class CepError(Exception):
    ...


class CepNotFound(CepError):
    ...


def clear_cep(cep: str):
    return re.sub(r"\D", "", str(cep))


def serializer_cep(cep: str):
    if len(cep) >= 5:
        return f"{cep[:5]}{cep[5:]:0<3}"
    return cep


def mask_cep(cep: str):
    cep = clear_cep(cep)
    if len(cep) >= 5:
        return f"{cep[:5]}-{cep[5:]:0<3}"
    return cep


class CepCordenadas(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CepLocation(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[CepCordenadas] = None


class CepConsultaV2(BaseModel):
    cep: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    service: Optional[str] = None
    location: Optional[CepLocation] = None


class CepConsultaV1(BaseModel):
    cep: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    service: Optional[str] = None


class Cep:
    CepNotFound = CepNotFound
    CepError = CepError

    def __init__(self, version):
        self.version = version

    def _get_url(self, cep: str):
        return f"https://brasilapi.com.br/api/cep/v{self.version}/{cep}"

    def _response(self, response, cep: str):
        if response.status_code == 200:
            return response.json()
        else:
            raise CepNotFound(f"CEP {mask_cep(cep)} não encontrado")

    def _serializer(self, data: dict):
        if self.version == 2:
            return CepConsultaV2(**data)
        return CepConsultaV1(**data)

    def get(self, cep: str):
        cep = serializer_cep(cep)
        url = self._get_url(cep)
        response = self._response(get(url), cep)
        return self._serializer(response)
