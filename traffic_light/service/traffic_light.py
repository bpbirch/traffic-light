import traffic_light.domain.models as models
from traffic_light.service.unit_of_work import AbstractTrafficLightUnitOfWork
import uuid


async def upsert_traffic_light(
    traffic_light: models.BaseTrafficLight,
    uow: AbstractTrafficLightUnitOfWork
) -> uuid.UUID:
    async with uow:
        light_id = await uow.traffic_light_repository.upsert_traffic_light(traffic_light)
        await uow.commit()
    return light_id


async def get_traffic_light(
    light_id: uuid.UUID,
    uow: AbstractTrafficLightUnitOfWork,
) -> models.BaseTrafficLight:
    async with uow:
        return await uow.traffic_light_repository.get_traffic_light(light_id)
