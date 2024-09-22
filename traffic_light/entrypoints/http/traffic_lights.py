from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from traffic_light.service.unit_of_work import AbstractTrafficLightUnitOfWork
from traffic_light.container import Container
import traffic_light.domain.models as models
import traffic_light.service.traffic_light as traffic_service_layer
import traffic_light.domain.exceptions as traffic_exceptions
import uuid


agents_router = APIRouter(
    prefix="/traffic-lights",
    tags=["traffic-lights"],
)


@agents_router.post("/")
@inject
async def upsert_traffic_light(
    request: Request,  # the request param will get used if we want to introduce an auth decorator
    traffic_light: models.BaseTrafficLightHTTP,
    uow: AbstractTrafficLightUnitOfWork = Depends(Provide[Container.uow]),
) -> uuid.UUID:
    try:
        return await traffic_service_layer.upsert_traffic_light(
            traffic_light=traffic_light, uow=uow
        )
    except traffic_exceptions.TrafficLightBaseException as ex:
        raise traffic_exceptions.HTTPTrafficLightValidationException(
            f"There was a problem validating your traffic light model: {ex.message}"
        )


@agents_router.get("/{light_id}")
@inject
async def get_traffic_light(
    request: Request,  # the request param will get used if we want to introduce an auth decorator
    light_id: uuid.UUID,
    uow: AbstractTrafficLightUnitOfWork = Depends(Provide[Container.uow]),
) -> models.BaseTrafficLightHTTP:
    try:
        return await traffic_service_layer.get_traffic_light(light_id=light_id, uow=uow)
    except traffic_exceptions.TrafficLightNotFoundException:
        raise traffic_exceptions.HTTPTrafficLightNotFoundException(
            f"TrafficLight with id {light_id} not found"
        )


# TODO: rest of CRUD for TrafficLight
