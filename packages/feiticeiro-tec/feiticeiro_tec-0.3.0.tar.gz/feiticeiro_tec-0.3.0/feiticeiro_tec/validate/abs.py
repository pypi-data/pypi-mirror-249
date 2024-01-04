from abc import ABC, abstractproperty
import re


def clean_value(value, ignore=False):
    if ignore:
        return value
    return re.sub(r"\D", "", value)


class AbsValidatorType(ABC):
    ...


class AbstractValidator(AbsValidatorType):
    @abstractproperty
    def validate(self, doc: str) -> bool:
        ...

    @abstractproperty
    def mask(self, doc="") -> str:
        ...


class REGEX(AbsValidatorType):
    CLEAR = False

    @abstractproperty
    def REGEX(self) -> re.compile:
        ...

    @abstractproperty
    def MASK_MATCH(self) -> str:
        ...

    def validate(self, value) -> bool:
        value = clean_value(value, not self.CLEAR)
        value_mask = self.mask(value)
        if not value or not value_mask:
            return False
        if value == clean_value(value_mask, not self.CLEAR):
            return True

    def mask(self, value) -> str:
        if isinstance(self.REGEX, str):
            self.REGEX = re.compile(self.REGEX)
        return self.REGEX.sub(self.MASK_MATCH, value)


class REGEXMATCH(AbsValidatorType):
    CLEAR = False

    @abstractproperty
    def REGEX(self) -> re.compile:
        ...

    @abstractproperty
    def MASK_MATCH(self) -> str:
        ...

    def validate(self, value) -> bool:
        if isinstance(self.REGEX, str):
            self.REGEX = re.compile(self.REGEX)
        if self.REGEX.match(value):
            return True
        return False

    def mask(self, value) -> str:
        if isinstance(self.REGEX, str):
            self.REGEX = re.compile(self.REGEX)
        return self.REGEX.sub(self.MASK_MATCH, value)


class AbstractValidate(ABC):
    CLEAR = False

    @abstractproperty
    def MSG_RAISE(self):
        ...

    @abstractproperty
    def VALIDATOR(self):
        ...

    def validate(self, value):
        """Valida o documento.
        raise ValueError: caso o documento seja inválido"""
        if not self.VALIDATOR().validate(clean_value(value, not self.CLEAR)):
            raise ValueError(self.MSG_RAISE)
        return True

    def mask(self, value):
        return self.VALIDATOR().mask(clean_value(value, not self.CLEAR))
