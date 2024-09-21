from tests.unit.test_utils import TrafficLightTestCaseWithContainerSingleton
import traffic_light.domain.models as models
import traffic_light.service.traffic_light as traffic_service_layer
import traffic_light.domain.exceptions as traffic_exceptions


class TrafficLightUnitTestCase(TrafficLightTestCaseWithContainerSingleton):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.traffic_light_input = models.BaseTrafficLightHTTP(
            green_time=10,
            yellow_time=5,
            red_time=10,
        )
        self.traffic_light = models.TrafficLightServiceLayerModel(**self.traffic_light_input.model_dump())

    async def test_upsert_and_get_traffic_light(self) -> None:
        light_id = await traffic_service_layer.upsert_traffic_light(
            traffic_light=self.traffic_light_input, uow=self.container.uow()
        )
        self.assertEqual(light_id, self.traffic_light.id)

        got_light_input = await traffic_service_layer.get_traffic_light(
            light_id=self.traffic_light.id, uow=self.container.uow(),
        )
        print(f'\ngot_light_input: {got_light_input}\n')
        print(f'\nself.traffic_light_input: {self.traffic_light_input}\n')
        self.assertEqual(got_light_input, self.traffic_light_input)

    async def test_increment_traffic_light_color(self) -> None:
        self.traffic_light.increment_signal_count()
        signal_count = self.traffic_light.signal_count
        self.assertEqual(signal_count, 1)

    async def test_get_traffic_light_color(self) -> None:
        got_green = self.traffic_light.get_color()
        print(f'\ngot_color: {got_green}\n')
        self.assertEqual(got_green, models.SupportedColor.GREEN)

        self.traffic_light.set_signal_count(10)
        got_yellow = self.traffic_light.get_color()
        self.assertEqual(got_yellow, models.SupportedColor.YELLOW)

        self.traffic_light.set_signal_count(15)
        got_red = self.traffic_light.get_color()
        self.assertEqual(got_red, models.SupportedColor.RED)

        # modular tests:
        self.traffic_light.set_signal_count(26)
        got_green = self.traffic_light.get_color()
        self.assertEqual(got_green, models.SupportedColor.GREEN)

        self.traffic_light.set_signal_count(35)
        got_yellow = self.traffic_light.get_color()
        self.assertEqual(got_yellow, models.SupportedColor.YELLOW)

        self.traffic_light.set_signal_count(41)
        got_red = self.traffic_light.get_color()
        self.assertEqual(got_red, models.SupportedColor.RED)

    def test_validation_errors(self) -> None:
        with self.assertRaises(traffic_exceptions.TrafficLightValidationException):
            _ = models.TrafficLightServiceLayerModel(green_time=-1)
        with self.assertRaises(traffic_exceptions.TrafficLightValidationException):
            _ = models.TrafficLightServiceLayerModel(yellow_time=-1)
        with self.assertRaises(traffic_exceptions.TrafficLightValidationException):
            _ = models.TrafficLightServiceLayerModel(red_time=-1)
        with self.assertRaises(traffic_exceptions.TrafficLightValidationException):
            _ = models.TrafficLightServiceLayerModel(green_time=0, yellow_time=0, red_time=0)
