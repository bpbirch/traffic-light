from pydantic import BaseModel, ConfigDict, Field, model_validator
from enum import Enum
from typing import Any, Dict, List, Optional
import datetime
import uuid
import traffic_light.domain.exceptions as traffic_exceptions


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


class HasUUID(BaseModel):
    id: uuid.UUID = Field(default_factory=generate_uuid)


class HasTimeStamps(BaseModel):
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc)
    )
    updated_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc)
    )

    model_config = ConfigDict(
        json_encoders={datetime.datetime: lambda v: v.isoformat()}
    )

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Override of BaseModel.model_dump, for supported DB storage format

        Returns:
            Dict[str, Any]: dumped BaseModel with fields and values
        """
        def serialize(value: Any) -> Any:
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            elif isinstance(value, dict):
                return {key: serialize(val) for key, val in value.items()}
            elif isinstance(value, list):
                return [serialize(item) for item in value]
            elif isinstance(value, BaseModel):
                return (
                    value.model_dump()
                )  # Recursively serialize nested Pydantic models
            return value

        original_dump = super().model_dump(*args, **kwargs)
        return {key: serialize(value) for key, value in original_dump.items()}


class SupportedSystem(str, Enum):
    TRAFFIC_LIGHT = "TRAFFIC LIGHT"

# class SpeedBasedTrafficHandler(BaseModel):
#     """potentially use this model to generate TrafficLight objects with times, based on speed

#     """
#     supported_system: SupportedSystem = SupportedSystem.TRAFFIC_LIGHT
#     def get_traffic_light(self, speed: int) -> "BaseTrafficLight":


class BaseTrafficLight(HasUUID, HasTimeStamps):
    supported_systems: List[SupportedSystem] = Field(default=[SupportedSystem.TRAFFIC_LIGHT])
    green_time: Optional[int] = Field(default=60)
    yellow_time: Optional[int] = Field(default=6)
    red_time: Optional[int] = Field(default=120)
    # cycle_repeat_amount would be used if we wanted to use multiple TrafficLight objects
    # to create a pattern throughout the day
    cycle_repeat_amount: Optional[int] = Field(default=None)
    repeat_indefinitely: Optional[bool] = Field(default=True)

    @model_validator(mode="before")
    def validate_times(cls, data: Any) -> Any:
        green_time = data.get("green_time")
        yellow_time = data.get("yellow_time")
        red_time = data.get("red_time")
        cycle_repeat_amount = data.get("cycle_repeat_amount")
        for color, timer in [("green_time", green_time), ("yellow_time", yellow_time), ("red_time", red_time)]:
            if not isinstance(timer, int):
                raise traffic_exceptions.TrafficLightBaseException(
                    f'{color} must be an instance of int, but type {type(timer)} was passed.'
                )
            if timer < 0:
                raise traffic_exceptions.TrafficLightBaseException(
                    f'{color} must be greater than zero, but {timer} was passed'
                )
        if cycle_repeat_amount is not None:
            if not isinstance(cycle_repeat_amount, int):
                raise traffic_exceptions.TrafficLightBaseException(
                    f'cycle_repeat_amount must be instance of int, but type {type(cycle_repeat_amount)} was passed.'
                )
            if cycle_repeat_amount < 0:
                raise traffic_exceptions.TrafficLightBaseException(
                    f'cycle_repeat_amount must be greater than zero, but {cycle_repeat_amount} was passed'
                )
        return data


class FlashingTrafficLight(BaseTrafficLight):
    green_flash_time: Optional[int] = Field(default=0)
    yellow_flash_time: Optional[int] = Field(default=0)
    red_flash_time: Optional[int] = Field(default=0)


class StopSignTrafficLight(FlashingTrafficLight):
    """Flashing reds after system crash; will repeat indefinitely"""
    red_flash_time: int = Field(default=1)
