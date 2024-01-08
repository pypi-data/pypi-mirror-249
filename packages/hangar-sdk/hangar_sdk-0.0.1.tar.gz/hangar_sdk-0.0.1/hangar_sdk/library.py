import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from rich import print
from rich.live import Live
from rich.tree import Tree

from .base import HangarScope
from .utils import print_status


class Config:
    mode = "create"


class HangarManager:
    objects = []

    @staticmethod
    def add(obj):
        HangarManager.objects.append(obj)

    @staticmethod
    def delete_objects():
        while HangarManager.objects:
            obj = HangarManager.objects.pop()
            del obj
            print("Object deleted.")


@dataclass(kw_only=True)
class Resource(ABC):
    name: str
    _resolved: bool = False

    def __post_init__(self):
        HangarManager.add(self)
        self.mode = Config.mode
        print(self.name, self.mode)

    def resolve(self, parent=None):
        pass


@dataclass(kw_only=True)
class CompositeResource(Resource, ABC):
    scope: HangarScope
    name: str
    mode: str = None
    _changed: bool = False
    _job_id: Optional[str] = None
    _resources: List[Resource] = field(default_factory=list)
    _dependencies: List[Resource] = field(default_factory=list)

    def __post_init__(self):
        HangarManager.add(self)
        self.mode = Config.mode

    def _depended_on_by(self, resource: Resource):
        resource._dependencies.append(self)

    def _depends_on(self, resource: Resource):
        self._dependencies.append(resource)

    def _get_ref(self):
        return {"!REF": True, "resourceId": self.name}

    async def _resolveDependencies(self):
        for dependency in self._dependencies:
            await dependency.resolve(self)

    @abstractmethod
    async def resolve(self, parent: Optional[Resource] = None):
        pass

    def __del__(self):
        self.scope.delete_resource(self.name)

    def delete(self):
        self.scope.delete_resource(self.name)

    async def poll_status(self):
        if self._job_id is None:
            raise Exception("No job id")

        response = None

        with Live(print_status(self.name, None)[0], refresh_per_second=4) as live:
            while True:
                if self._job_id == "no-change":
                    tree = Tree(self.name)
                    tree.add("No change")
                    live.update(tree)
                    self._changed = False
                    break
                self._changed = True

                response = self.scope.get_status(self._job_id)
                # print(response)
                await asyncio.sleep(1)

                if response.status_code != 200:
                    raise Exception(response.text)

                status = response.json()
                render, _, errors = print_status(self.name, status)

                live.update(render)

                if response.json() and response.json()["completed"] is True:
                    break

                if errors and len(errors) > 0:
                    raise Exception(f"Errors occurred: {errors}")

        return response.json() if response else None

    @property
    def state(self):
        return self.scope.get_state(self.name)
