from multiprocessing import Process
from typing import Any
from uuid import uuid4
from loguru import logger
from datetime import datetime
import time
from typing import List


class Processo(Process):
    def __init__(
        self,
        name,
        target,
        group=None,
        daemon=True,
        uuid=None,
        description="",
        args=[],
        kwargs={},
    ):
        super().__init__(
            name=name,
            target=target,
            daemon=daemon,
            args=args,
            kwargs=kwargs,
        )
        self.uuid = None
        self.group = group
        self.target = target
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = uuid4()
        self.is_task = True
        self.last_run = None
        self.stoped = None
        self.description = description
        self.args = args
        self.kwargs = kwargs

    @property
    def is_running(self):
        return self.is_alive()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.target(*args, **kwds)

    def heranca(self):
        return {
            "name": self.name,
            "target": self.target,
            "group": self.group,
            "daemon": self.daemon,
            "uuid": self.uuid,
            "description": self.description,
            "args": self.args,
            "kwargs": self.kwargs,
        }

    def __repr__(self) -> str:
        return '<Processo name:"{}" uuid:"{}" group:"{}"/>'.format(
            self.name, self.uuid, self.group
        )

    def start(self) -> None:
        logger.info(f"{self} Iniciado!")
        self.last_run = datetime.utcnow()
        return super().start()

    def terminate(self) -> None:
        logger.info(f"{self} Terminado!")
        self.stoped = datetime.utcnow()
        return super().terminate()


class ManagerProcess:
    _storage = {}

    def _add(self, process: Process, group: str = None):
        """Adicionar um processo no setlist do group"""
        self._storage.setdefault(group, set()).add(process)

    def remove(self, process: Process, group: str = None):
        """Remove um processo do setlit do group"""
        process.is_alive() and process.terminate()
        self._storage.get(group, set()).remove(process)

    def restart(self, uuid):
        old = self.find_by_uuid(uuid)
        processo = self.new(
            **old.heranca(),
        )
        self.remove(old, old.group)
        processo.start()
        return processo

    def find_by_function(self, function):
        for processo in self._get_all():
            if processo.target == function:
                return processo

    def task(
        self,
        *args,
        name=None,
        group="decorador",
        description="",
        daemon=True,
        uuid=None,
        **kwargs,
    ):
        def wrapper(target):
            processo = self.new(
                name=name or target.__name__,
                target=target,
                group=group,
                description=description or target.__doc__ or "",
                daemon=daemon,
                uuid=uuid,
                *args,
                **kwargs,
            )
            return processo

        return wrapper

    def new(
        self,
        name,
        target,
        group="default",
        description="",
        daemon=True,
        uuid=None,
        args=[],
        kwargs={},
    ):
        processo = Processo(
            uuid=uuid,
            name=name,
            target=target,
            group=group,
            daemon=daemon,
            description=description,
            args=args,
            kwargs=kwargs,
        )
        self._add(processo, group)
        logger.success(f"{processo} Criado!")
        return processo

    def find_by_uuid(self, uuid):
        for processo in self._get_all():
            if str(processo.uuid) == str(uuid):
                return processo

    def stop(self, uuid):
        processo = self.find_by_uuid(uuid)
        if processo:
            processo.terminate()
            return processo
        logger.warning(f"Processo com uuid '{uuid}' não encontrado!")
        return False

    @property
    def groups(self):
        return tuple(self._storage.keys())

    @classmethod
    def loop(cls):
        while True:
            time.sleep(1)

    def _get_all(self) -> List[Process]:
        for grupo in self._storage.values():
            for processo in grupo:
                yield processo

    def _get_all_by_group(self, group):
        for processo in self._storage.get(group, set()):
            yield processo

    def _get_process(self, group=None):
        if group:
            processos = self._get_all_by_group(group=group)
        else:
            processos = self._get_all()
        for processo in processos:
            yield processo

    def start(self, group=None):
        processos = self._get_process(group=group)
        for processo in processos:
            processo.start()

    def wait(self, group=None):
        processos = self._get_process(group=group)
        for processo in processos:
            processo.join()

    def __getitem__(self, name):
        return tuple(self._get_process(name))

    def __iter__(self):
        return self._get_process()
