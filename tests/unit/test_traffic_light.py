from tests.unit.test_utils import TrafficLightTestCaseWithContainerSingleton
import traffic_light.domain.models as models
import traffic_light.service.traffic_light as traffic_service_layer


class TrafficLightUnitTestCase(TrafficLightTestCaseWithContainerSingleton):
    async def test_upsert_and_get_traffic_light(self) -> None:
        traffic_light = models.BaseTrafficLight(
            green_time=10,
            yellow_time=5,
            red_time=10,
        )
        light_id = await traffic_service_layer.upsert_traffic_light(
            traffic_light=traffic_light, uow=self.container.uow()
        )
        self.assertEqual(light_id, traffic_light.id)

        got_light = await traffic_service_layer.get_traffic_light(
            light_id=traffic_light.id, uow=self.container.uow(),
        )
        self.assertEqual(got_light, traffic_light)
