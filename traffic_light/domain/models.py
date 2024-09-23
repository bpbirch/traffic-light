import abc
import datetime
import uuid
from enum import Enum
from typing import Any, List, Optional, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

import traffic_light.domain.exceptions as traffic_exceptions


class SupportedColor(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"
    BLUE = "BLUE"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"


class SupportedSystem(str, Enum):
    """enum for extensibility, in the case that we want to query for lights,
    based on supported systems (party lights, traffic lights, airport control lights, etc.)

    """

    TRAFFIC_LIGHT = "TRAFFIC LIGHT"


class SupportedLightType(str, Enum):
    STANDARD = "STANDARD"


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


# pydantic models for input and output at HTTP layer - for extensibility if we want to
# run as a microservice supported web API


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


# class SpeedBasedTrafficHandler(BaseModel):
#     """potentially use this model to generate TrafficLight objects with times, based on speed

#     """
#     supported_system: SupportedSystem = SupportedSystem.TRAFFIC_LIGHT
#     def get_traffic_light(self, speed: int) -> "BaseTrafficLight":


class BaseTrafficLightHTTP(HasUUID, HasTimeStamps):
    supported_systems: List[SupportedSystem] = Field(
        default=[SupportedSystem.TRAFFIC_LIGHT]
    )
    supported_colors: List[SupportedColor] = Field(
        default=[SupportedColor.GREEN, SupportedColor.YELLOW, SupportedColor.RED]
    )
    supported_light_type: SupportedLightType = Field(
        default=SupportedLightType.STANDARD
    )
    green_time: int = Field(default=60)
    yellow_time: int = Field(default=6)
    red_time: int = Field(default=120)
    # cycle_repeat_amount would be used if we wanted to use multiple TrafficLight objects
    # to create a pattern throughout the day
    cycle_repeat_amount: Optional[int] = Field(default=None)
    signal_count: Optional[int] = Field(default=0)

    @model_validator(mode="before")
    def validate_times(cls, data: Any) -> Any:
        """customized error handling for validation errors, so we're not
        just raising generic pydantic validation errors

        Args:
            data (Any): model data

        Raises:
            traffic_exceptions.HTTPTrafficLightValidationException: _description_
            traffic_exceptions.HTTPTrafficLightValidationException: _description_
            traffic_exceptions.HTTPTrafficLightValidationException: _description_
            traffic_exceptions.HTTPTrafficLightValidationException: _description_

        Returns:
            Any: model data
        """
        green_time = data.get("green_time")
        yellow_time = data.get("yellow_time")
        red_time = data.get("red_time")
        cycle_repeat_amount = data.get("cycle_repeat_amount")
        for color, timer in [
            ("green_time", green_time),
            ("yellow_time", yellow_time),
            ("red_time", red_time),
        ]:
            if not isinstance(timer, int):
                raise traffic_exceptions.HTTPTrafficLightValidationException(
                    f"{color} must be an instance of int, but type {type(timer)} was passed."
                )
            if timer < 0:
                raise traffic_exceptions.HTTPTrafficLightValidationException(
                    f"{color} must be greater than zero, but {timer} was passed"
                )
        if green_time + yellow_time + red_time <= 0:
            raise traffic_exceptions.HTTPTrafficLightValidationException(
                "total times for green, yellow, and red times must be greater than zero"
            )
        if cycle_repeat_amount is not None:
            if not isinstance(cycle_repeat_amount, int):
                raise traffic_exceptions.HTTPTrafficLightValidationException(
                    f"cycle_repeat_amount must be instance of int, but type {type(cycle_repeat_amount)} was passed."
                )
            if cycle_repeat_amount < 0:
                raise traffic_exceptions.HTTPTrafficLightValidationException(
                    f"cycle_repeat_amount must be greater than zero, but {cycle_repeat_amount} was passed"
                )
        return data


class BaseFlashingTrafficLightHTTP(BaseTrafficLightHTTP):
    """
    This model is used for traffic signals that involve a flashing light component for one or more colors
    """

    green_flash_time: Optional[int] = Field(default=0)
    yellow_flash_time: Optional[int] = Field(default=0)
    red_flash_time: Optional[int] = Field(default=0)

    # TODO: write algorithmic method for determining whether a light is flashing or not at any given signal count
    # - out of scope for this project

    @model_validator(mode="before")
    def validate_flashing_times(cls, data: Any) -> Any:
        green_flash_time = data.get("green_flash_time")
        yellow_flash_time = data.get("yellow_flash_time")
        red_flash_time = data.get("red_flash_time")
        green_time = data.get("green_time")
        yellow_time = data.get("yellow_time")
        red_time = data.get("red_time")

        for color, flash_timer, color_timer in [
            ("green_flash_time", green_flash_time, green_time),
            ("yellow_flash_time", yellow_flash_time, yellow_time),
            ("red_flash_time", red_flash_time, red_time),
        ]:
            if not isinstance(flash_timer, int):
                raise traffic_exceptions.TrafficLightValidationException(
                    f"{color} must be an instance of int, but type {type(flash_timer)} was passed."
                )
            if flash_timer < 0:
                raise traffic_exceptions.TrafficLightValidationException(
                    f"{color} must be greater than zero, but {flash_timer} was passed"
                )
            # following validation is because a flash timer for a color must be less than the total time for that color
            # eg a light can't flash green for longer than the light remains green
            if flash_timer > color_timer:
                raise traffic_exceptions.TrafficLightValidationException(
                    f"flash_timer must be less than color_timer, but for color {color}, flash_timer {flash_timer} is greater than {color_timer}"
                )

        return data


class BaseStopSignTrafficLightHTTP(BaseTrafficLightHTTP):
    """Flashing reds after system crash; will repeat indefinitely"""

    red_flash_time: int = Field(default=1)


# service layer models (business logic should not live inside of pydantic models)


class BaseTrafficLightServiceLayerModel(abc.ABC):
    def __init__(
        self,
        id: uuid.UUID,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        supported_systems: List[SupportedSystem],
        supported_colors: List[SupportedColor],
        supported_light_type: SupportedLightType,
        green_time: int,
        yellow_time: int,
        red_time: int,
        cycle_repeat_amount: Optional[int] = None,
        signal_count: int = 0,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.supported_systems = supported_systems
        self.supported_colors = supported_colors
        self.supported_light_type = supported_light_type
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.red_time = red_time
        self.total_time: Optional[int] = None
        self.cycle_repeat_amount = cycle_repeat_amount
        self.signal_count = signal_count

    @abc.abstractmethod
    def get_color(self) -> SupportedColor:
        """
        Current color, based on signal time and total signal time (based on modular signal  time)
        """
        ...

    @abc.abstractmethod
    def to_pydantic(self) -> BaseTrafficLightHTTP:
        """
        Return the analogous http pydantic model from the service layer instance
        """

    def increment_signal_count(self, steps: int = 1) -> None:
        """
        Increment self.signal_count by steps

        Args:
            steps (Optional[int], optional): steps to increment by. Defaults to 1.
        """
        self.signal_count += steps

    def set_signal_count(self, total_count: int) -> None:
        """
        Set self.signal_count to absolute value total_count

        Args:
            total_count (int): _description_

        Returns:
            int: total step count
        """
        self.signal_count = total_count

    def get_modular_signal_count(self) -> int:
        """
        Method for determining which color light is set to, based on self.signal_count and total_steps, using modular arithmetic

        Returns:
            int: modular count
        """
        total_time = cast(int, self.total_time)
        signal_count = cast(int, self.signal_count)
        mod_signal_count = signal_count % total_time
        return mod_signal_count

    def __repr__(self) -> str:
        return f"<BaseTrafficLightServiceLayerModel :: {vars(self)}>"


class TrafficLightServiceLayerModel(BaseTrafficLightServiceLayerModel):
    def __init__(
        self,
        id: uuid.UUID = uuid.uuid4(),
        created_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc),
        updated_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc),
        supported_systems: List[SupportedSystem] = [SupportedSystem.TRAFFIC_LIGHT],
        supported_colors: List[SupportedColor] = [
            SupportedColor.GREEN,
            SupportedColor.YELLOW,
            SupportedColor.RED,
        ],
        supported_light_type: SupportedLightType = SupportedLightType.STANDARD,
        green_time: int = 60,
        yellow_time: int = 6,
        red_time: int = 120,
        cycle_repeat_amount: Optional[int] = None,
        signal_count: int = 0,
    ) -> None:
        for color, timer in [
            ("green_time", green_time),
            ("yellow_time", yellow_time),
            ("red_time", red_time),
        ]:
            if not isinstance(timer, int):
                raise traffic_exceptions.TrafficLightValidationException(
                    f"{color} must be an instance of int, but type {type(timer)} was passed."
                )
            if timer < 0:
                raise traffic_exceptions.TrafficLightValidationException(
                    f"{color} must be greater than zero, but {timer} was passed"
                )
        self.total_time = green_time + yellow_time + red_time
        if self.total_time <= 0:
            raise traffic_exceptions.TrafficLightValidationException(
                "total times for green, yellow, and red times must be greater than zero"
            )
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.supported_systems = supported_systems
        self.supported_colors = supported_colors
        self.supported_light_type = supported_light_type
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.red_time = red_time
        self.cycle_repeat_amount = cycle_repeat_amount
        self.signal_count = signal_count

    def get_modular_signal_count(self) -> int:
        total_time = cast(int, self.total_time)
        signal_count = cast(int, self.signal_count)
        mod_signal_count = signal_count % total_time
        return mod_signal_count

    def get_color(self) -> SupportedColor:
        green_range = range(self.green_time)
        yellow_range = range(self.green_time, self.green_time + self.yellow_time)
        red_range = range(
            self.green_time + self.yellow_time, cast(int, self.total_time)
        )
        signal_count = self.signal_count
        mod_signal_count = self.get_modular_signal_count()

        if mod_signal_count in green_range:
            return SupportedColor.GREEN
        elif mod_signal_count in yellow_range:
            return SupportedColor.YELLOW
        elif mod_signal_count in red_range:
            return SupportedColor.RED
        else:
            raise traffic_exceptions.TrafficLightValidationException(
                f"Modular count fell outside of signal color ranges: signal_count = {signal_count}, mod_signal_count = {mod_signal_count}"
            )

    def to_pydantic(self) -> BaseTrafficLightHTTP:
        return BaseTrafficLightHTTP(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            supported_systems=self.supported_systems,
            supported_colors=self.supported_colors,
            green_time=self.green_time,
            yellow_time=self.yellow_time,
            red_time=self.red_time,
            cycle_repeat_amount=self.cycle_repeat_amount,
            signal_count=self.signal_count,
        )


class FlashingTrafficLightServiceLayerModel(TrafficLightServiceLayerModel):
    """
    TODO: implement for flashing light extensibility at service layer
    """

    pass


class StopSignTrafficLightServiceLayerModel(FlashingTrafficLightServiceLayerModel):
    """
    TODO: implement for flashign red lights for hazard at service layer
    """
