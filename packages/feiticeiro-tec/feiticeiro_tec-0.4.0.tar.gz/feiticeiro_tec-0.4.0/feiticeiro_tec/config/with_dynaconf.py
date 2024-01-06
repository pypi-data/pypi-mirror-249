from dynaconf import Dynaconf
from loguru import logger
from pydantic import BaseModel
from enum import Enum
import os


class EnvEnum(Enum):
    DEV = "DEV"
    PRD = "PRD"


class TypeEnv(BaseModel):
    ENV: EnvEnum
    DEBUG: bool = False

    @classmethod
    def create_config(cls, settings, env):
        SETTINGS_DICT = settings.as_dict()
        ENV_ROOT = dict(os.environ)
        DEFAULT_SETTINGS = SETTINGS_DICT.pop("DEFAULT", {})
        ENV_SETTINGS = SETTINGS_DICT.pop(env, {})

        obj = cls(
            **{
                **DEFAULT_SETTINGS,
                **ENV_SETTINGS,
                **SETTINGS_DICT,
                **ENV_ROOT,
                "ENV": env,
            }
        )
        obj._settings = settings
        return obj

    @classmethod
    def load_env(cls, default, env, settings_files=[], prefix=""):
        return cls.create_config(
            Dynaconf(
                environments=True,
                envvar_prefix=prefix,
                default_env=default,
                env=env,
                settings_files=settings_files,
            ),
            env=env,
        )

    def show(self):
        text_env = f"VARIAVEIS DE AMBIENTE: {self.ENV.value}\n"
        envs = [f"{key} = {value}" for key, value in dict(self).items()]
        text_env += "\n".join(envs)
        logger.warning(text_env)
