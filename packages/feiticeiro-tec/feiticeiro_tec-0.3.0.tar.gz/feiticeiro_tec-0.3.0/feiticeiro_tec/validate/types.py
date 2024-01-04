from validate_docbr import CPF, CNPJ
import re
from .abs import AbstractValidator, REGEX, REGEXMATCH


class CPFCNPJ(AbstractValidator):
    def validate(self, doc) -> bool:
        doc = re.sub(r"\D", "", doc)
        if len(doc) == 11:
            return CPF().validate(doc)
        return CNPJ().validate(doc)

    def mask(self, doc="") -> str:
        doc = re.sub(r"\D", "", doc)
        if len(doc) == 11:
            return CPF().mask(doc)
        return CNPJ().mask(doc)


class INCRICAOMUNICIPAL(REGEX):
    CLEAR = True
    REGEX = r"(\d{3})(\d{3})(\d)"
    MASK_MATCH = r"\1.\2-\3"


class EMAIL(REGEXMATCH):
    REGEX = r"([\w\W]+)(@)([\w\W]+)(.)([\w\W]+)"
    MASK_MATCH = r"\1\2\3\4\5"

    def validate(self, value) -> bool:
        return super().validate(value) and "." in value and "@" in value
