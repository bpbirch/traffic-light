from traffic_light.adapters.repositories.protocols import TrafficLightRepository
import traffic_light.domain.models as models
import uuid
from typing import Dict
import traffic_light.domain.exceptions as traffic_exceptions


class InMemoryTrafficLightRepository(TrafficLightRepository):
    _traffic_lights: Dict[uuid.UUID, models.TrafficLightServiceLayerModel] = {}

    async def upsert_traffic_light(self, traffic_light: models.TrafficLightServiceLayerModel) -> uuid.UUID:
        self._traffic_lights[traffic_light.id] = traffic_light
        return traffic_light.id

    async def get_traffic_light(self, light_id: uuid.UUID) -> models.TrafficLightServiceLayerModel:
        traffic_light = self._traffic_lights.get(light_id)
        if not traffic_light:
            raise traffic_exceptions.TrafficLightNotFoundException(
                f'TrafficLight with id {light_id} not found'
            )
        return traffic_light
