from dependency_injector import containers, providers

from traffic_light.adapters.repositories.in_memory import InMemoryTrafficLightRepository
from traffic_light.adapters.repositories.protocols import TrafficLightRepository
from traffic_light.config.configuration import settings
from traffic_light.service.unit_of_work import InMemoryUnitOfWork


class Container(containers.DeclarativeContainer):
    """
    The current DI Container implementation injects the following:
    - Unit of Work (UOW): In-Memory and Mongodb

    """

    # Define modules to "wire up" with DI
    wiring_config = containers.WiringConfiguration(
        packages=[
            "traffic_light.entrypoints.http",
            "traffic_light.service",
        ]
    )

    # Parse the settings
    config = providers.Configuration()
    config.from_dict(settings.model_dump(by_alias=True))

    # required for the InMemoryUnitOfWork only.
    service_repo = providers.Dependency(
        instance_of=TrafficLightRepository,  # type: ignore
        default=InMemoryTrafficLightRepository(),  # type: ignore
    )

    # selects an implementation of the UoW based on the config
    uow = providers.Selector(
        config.db_type,
        **{  # type: ignore
            "inmemory": providers.Factory(InMemoryUnitOfWork, service_repo),
            # here is where we would add support for other repos (postgers, mongo)
        },
    )


class ContainerSingleton:
    _instance = None

    @classmethod
    def reset(cls) -> Container:
        cls._instance = Container()
        return cls._instance

    @classmethod
    def get_instance(cls) -> Container:
        if cls._instance is None:
            cls._instance = Container()
        return cls._instance
