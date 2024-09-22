from typing import Protocol, runtime_checkable
import traffic_light.domain.models as models
import uuid


# BEGIN write repository
@runtime_checkable
class TrafficLightWriteRepository(Protocol):
    async def upsert_traffic_light(
        self, traffic_light: models.TrafficLightServiceLayerModel
    ) -> uuid.UUID:
        """Create or Update a TrafficLight"""


# BEGIN read repository
@runtime_checkable
class TrafficLightReadRepository(Protocol):
    async def get_traffic_light(
        self, light_id: uuid.UUID
    ) -> models.TrafficLightServiceLayerModel:
        """Get TrafficLight"""


@runtime_checkable
class TrafficLightRepository(
    TrafficLightWriteRepository, TrafficLightReadRepository, Protocol
):
    pass
