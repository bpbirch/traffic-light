import traffic_light.domain.exceptions as traffic_exceptions
from traffic_light.domain import models
import click


LIGHT_CIRCLE = """
       ***
   ** ****** **
 * ************ *
* ************** *
* ************** *
 * ************ *
   ** ****** **
       ***
"""


# We can extend this object to handle different kinds of lights
class TrafficLightHandler:
    def __init__(
        self,
        traffic_light: models.BaseTrafficLightServiceLayerModel,
        light_circle: str = LIGHT_CIRCLE,
    ):
        self.light_circle = light_circle
        self.traffic_light = traffic_light

    def set_traffic_light_object(
        self, traffic_light: models.BaseTrafficLightServiceLayerModel
    ) -> None:
        self.traffic_light = traffic_light

    def get_display(self) -> str:
        if (
            self.traffic_light.supported_light_type
            == models.SupportedLightType.STANDARD
        ):
            light_color = self.traffic_light.get_color()
            if light_color == models.SupportedColor.GREEN:
                light = click.style(self.light_circle, fg="green")
                displayed = f"\n{light}\n{self.light_circle}\n{self.light_circle}"
            if light_color == models.SupportedColor.YELLOW:
                light = click.style(self.light_circle, fg="yellow")
                displayed = f"\n{self.light_circle}\n{light}\n{self.light_circle}"
            if light_color == models.SupportedColor.RED:
                light = click.style(self.light_circle, fg="red")
                displayed = f"\n{self.light_circle}\n{self.light_circle}\n{light}"
            return displayed
        else:
            raise traffic_exceptions.TrafficLightValidationException(
                f"light type {self.traffic_light.supported_light_type} for traffic_light not supported"
            )
