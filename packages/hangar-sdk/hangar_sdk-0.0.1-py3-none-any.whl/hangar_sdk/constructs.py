import os
import tarfile
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

from pydantic import BaseModel

from .base import HangarScope
from .library import CompositeResource


class SourceInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, source):
        pass


@dataclass
class Asset(CompositeResource):
    scope: HangarScope
    name: str
    source: SourceInterface

    def __post_init__(self):
        super().__post_init__()
        self._depends_on(self.source)

    async def resolve(self, parent=None):
        await self._resolveDependencies()

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True

        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            await self._resolveDependencies()
            return

        if not self._resolved:
            job_id = self.scope.add_construct(
                {
                    "config": {
                        "construct": "asset",
                        "name": self.name,
                        "source": {"!REF": True, "resourceId": self.source.name},
                    },
                    "resourceId": self.name,
                },
                force_change=to_change,
            )

            self._job_id = job_id
            await self.poll_status()

            self._resolved = True

    def sync(self, token=None):
        if self.mode == "delete":
            # self.scope.delete_resource(self.name)
            return
        return self.scope.execute_action(
            self.name, "sync", {"token": token} if token is not None else {}
        )


@dataclass
class DirPath(CompositeResource, SourceInterface):
    path: str

    async def resolve(self, parent=None):
        await self._resolveDependencies()
        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            return

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True

        if self._resolved:
            return

        if os.path.exists(self.path):
            with tempfile.TemporaryDirectory() as tmpdirname:
                with tarfile.open(f"{tmpdirname}/source.tar.gz", "w:gz") as tar:
                    tar.add(self.path, arcname=os.path.basename(self.path))

        self._resolved = True
        self._changed = True


@dataclass
class GitHubRepo(CompositeResource, SourceInterface):
    scope: HangarScope
    name: str
    repo: str
    branch: str

    async def resolve(self, parent=None):
        await self._resolveDependencies()

        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            return

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True
        if not self._resolved:
            job_id = self.scope.add_construct(
                {
                    "config": {
                        "construct": "githubrepo",
                        "name": self.name,
                        "repository": self.repo,
                        "branch": self.branch,
                    },
                    "resourceId": self.name,
                },
                force_change=to_change,
            )
            self._job_id = job_id

            await self.poll_status()

            self._resolved = True


class BuilderInterface(ABC):
    builderType: str

    @abstractmethod
    def __init__(self, builder):
        pass


@dataclass
class BuildkitBuilder(CompositeResource, BuilderInterface):
    scope: HangarScope
    name: str
    builder_type = "buildkit"

    async def resolve(self, parent=None):
        await self._resolveDependencies()
        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            return

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True

        if not self._resolved:
            job_id = self.scope.add_construct(
                {
                    "config": {"construct": "buildkit", "name": self.name},
                    "resourceId": self.name,
                },
                force_change=to_change,
            )

            self._job_id = job_id

            await self.poll_status()

            self._resolved = True


class RegistryInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, builder):
        pass


@dataclass
class Registry(CompositeResource, RegistryInterface):
    scope: HangarScope
    name: str

    async def resolve(self, parent=None):
        await self._resolveDependencies()

        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            return

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True

        if not self._resolved:
            job_id = self.scope.add_construct(
                {
                    "config": {"construct": "ecr", "name": self.name},
                    "resourceId": self.name,
                },
                force_change=to_change,
            )

            self._job_id = job_id

            await self.poll_status()

            self._resolved = True


@dataclass
class ContainerBuilder(CompositeResource):
    name: str
    asset: Asset
    builder: BuilderInterface
    registry: RegistryInterface

    def __post_init__(self):
        super().__post_init__()
        self._depends_on(self.asset)
        self._depends_on(self.builder)
        self._depends_on(self.registry)

    async def resolve(self, parent=None):
        await self._resolveDependencies()
        # print(self.mode)
        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            return

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True
        if self._resolved:
            return
        if not self._resolved:
            job_id = self.scope.add_construct(
                {
                    "config": {
                        "construct": "codebuild",
                        "name": self.name,
                        "asset": self.asset._get_ref(),
                        "builder": self.builder._get_ref(),
                        "registry": self.registry._get_ref(),
                    },
                    "resourceId": self.name,
                },
                force_change=to_change,
            )

            self._job_id = job_id

            await self.poll_status()

            self._resolved = True

    def build(self, build_context=None):
        if self.mode == "delete":
            # self.scope.delete_resource(self.name)
            return

        return self.scope.execute_action(
            self.name,
            "build",
            {
                "build_context": build_context
                if build_context is not None
                else self.name
            },
        )


class PortMappings(BaseModel):
    containerPort: int
    hostPort: int


@dataclass
class Container(CompositeResource):
    source: Registry
    tag: str
    startCommand: str = None
    portMappings: List[PortMappings] = None

    def __post_init__(self):
        super().__post_init__()
        self._depends_on(self.source)

    async def resolve(self, parent=None):
        await self._resolveDependencies()
        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            return

        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True
        if self._resolved:
            return
        if not self._resolved:
            job_id = self.scope.add_construct(
                {
                    "config": {
                        "construct": "container",
                        "name": self.name,
                        "registry": self.source._get_ref(),
                        "tag": self.tag,
                        "startCommand": self.startCommand.split(" ")
                        if self.startCommand is not None
                        else None,
                        "portMappings": [
                            mapping.model_dump() for mapping in self.portMappings
                        ]
                        if self.portMappings is not None
                        else None,
                    },
                    "resourceId": self.name,
                },
                force_change=to_change,
            )

            self._job_id = job_id

            await self.poll_status()

            self._resolved = True


@dataclass
class Service(CompositeResource):
    name: str
    container: Container
    environmentVariables: Dict[str, str] | None = None

    def __post_init__(self):
        super().__post_init__()
        self._depends_on(self.container)

    async def resolve(self, parent=None):
        await self._resolveDependencies()
        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True

        if self._resolved:
            return
        self._changed = to_change

        self._resolved = True


def env_vars_dict_to_str(env_vars: Dict[str, str]):
    return "\n".join([f"{k}={v}" for k, v in env_vars.items()])


@dataclass
class Cluster(CompositeResource):
    name: str
    services: List[Service]

    def __post_init__(self):
        super().__post_init__()
        for service in self.services:
            self._depends_on(service)

    def log(self, path=""):
        if self.mode == "delete":
            # self.scope.delete_resource(self.name)
            return
        return self.scope.get_logs(self.name, path)

    async def resolve(self, parent=None):
        if self.mode == "delete":
            self.scope.delete_resource(self.name)
            await self._resolveDependencies()
            return
        await self._resolveDependencies()
        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True
        if self._resolved:
            return

        thing = {
            "resourceId": self.name,
            "config": {
                "construct": "cluster",
                "name": self.name,
                "services": [
                    {
                        "name": s.name,
                        "container": s.container._get_ref(),
                        "environment_variables": env_vars_dict_to_str(
                            s.environmentVariables
                        )
                        if s.environmentVariables
                        else "",
                    }
                    for s in self.services
                ],
            },
        }
        job_id = self.scope.add_construct(thing, force_change=to_change)
        self._job_id = job_id

        await self.poll_status()

        self._resolved = True
