import abc
from typing import Any

from traffic_light.adapters.repositories.protocols import TrafficLightRepository


class AbstractUnitOfWork(abc.ABC):
    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class AbstractTrafficLightUnitOfWork(AbstractUnitOfWork, abc.ABC):
    traffic_light_repository: TrafficLightRepository


class InMemoryUnitOfWork(AbstractTrafficLightUnitOfWork):
    def __init__(self, repository: TrafficLightRepository) -> None:
        self.traffic_light_repository = repository
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> AbstractUnitOfWork:
        return await super().__aenter__()

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True
