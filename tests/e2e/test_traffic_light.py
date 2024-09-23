import traffic_light.domain.exceptions as traffic_exceptions
import traffic_light.domain.models as models
import traffic_light.service.traffic_light as traffic_service_layer
from tests.unit.test_utils import TrafficLightTestCaseWithContainerSingleton


class TrafficLightUnitTestCase(TrafficLightTestCaseWithContainerSingleton):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.traffic_light_input = models.BaseTrafficLightHTTP(
            green_time=10,
            yellow_time=5,
            red_time=10,
        )
        self.traffic_light = models.TrafficLightServiceLayerModel(
            **self.traffic_light_input.model_dump()
        )

    async def test_upsert_and_get_traffic_light(self) -> None:
        light_id = await traffic_service_layer.upsert_traffic_light(
            traffic_light=self.traffic_light_input, uow=self.container.uow()
        )
        self.assertEqual(light_id, self.traffic_light.id)

        got_light_input = await traffic_service_layer.get_traffic_light(
            light_id=self.traffic_light.id,
            uow=self.container.uow(),
        )
        print(f"\ngot_light_input: {got_light_input}\n")
        print(f"\nself.traffic_light_input: {self.traffic_light_input}\n")
        self.assertEqual(got_light_input, self.traffic_light_input)

    async def test_validation_errors(self) -> None:
        with self.assertRaises(traffic_exceptions.HTTPTrafficLightValidationException):
            _ = models.BaseTrafficLightHTTP(green_time=-1)
        with self.assertRaises(traffic_exceptions.HTTPTrafficLightValidationException):
            _ = models.BaseTrafficLightHTTP(yellow_time=-1)
        with self.assertRaises(traffic_exceptions.HTTPTrafficLightValidationException):
            _ = models.BaseTrafficLightHTTP(yellow_time=-1)
        with self.assertRaises(traffic_exceptions.HTTPTrafficLightValidationException):
            _ = models.BaseTrafficLightHTTP(green_time=0, yellow_time=0, red_time=0)
        with self.assertRaises(traffic_exceptions.HTTPTrafficLightValidationException):
            _ = models.BaseTrafficLightHTTP(green_time="this is not an int")
