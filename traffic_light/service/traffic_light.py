import traffic_light.domain.models as models
from traffic_light.service.unit_of_work import AbstractTrafficLightUnitOfWork
import uuid


async def upsert_traffic_light(
    traffic_light: models.BaseTrafficLightHTTP, uow: AbstractTrafficLightUnitOfWork
) -> uuid.UUID:
    async with uow:
        sl_model = models.TrafficLightServiceLayerModel(**traffic_light.model_dump())
        light_id = await uow.traffic_light_repository.upsert_traffic_light(sl_model)
        await uow.commit()
    return light_id


async def get_traffic_light(
    light_id: uuid.UUID,
    uow: AbstractTrafficLightUnitOfWork,
) -> models.BaseTrafficLightHTTP:
    async with uow:
        sl_model = await uow.traffic_light_repository.get_traffic_light(light_id)
        return sl_model.to_pydantic()
