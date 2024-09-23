from click.testing import CliRunner
from traffic_light.service.traffic_light_cli import (
    run_traffic_light,
)  # Adjust the import to your module's name
from unittest import TestCase
from traffic_light.service.handlers.traffic_light_handler import LIGHT_CIRCLE


class ClickCLITestCast(TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    # note on all tests: the plain text 'n' is to make sure we're not repeating indefinitely
    def test_valid_input(self) -> None:
        # Test norvalidmal input
        result = self.runner.invoke(run_traffic_light, input="1\n1\n1\nn\n")
        light_circle_output = result.output.count(LIGHT_CIRCLE)
        # we printed 3 traffic lights, so divide by 3 for expected
        expected_lights = light_circle_output / 3
        self.assertEqual(expected_lights, 3)
        self.assertIn(LIGHT_CIRCLE, result.output)
        self.assertIn("The configurations for colors are:", result.output)
        self.assertIn("green: 1 seconds", result.output)
        self.assertIn("yellow: 1 seconds", result.output)
        self.assertIn("red: 1 seconds", result.output)

    def test_q_exit(self) -> None:
        # Test exiting with 'q'
        result = self.runner.invoke(run_traffic_light, input="q\n")
        self.assertIn("Exiting Traffic Light Simulator", result.output)

    def test_invalid_green_time(self) -> None:
        # Test invalid input for green time
        result = self.runner.invoke(run_traffic_light, input="-1\n1\n0\n0\nn\n")
        print(f"\noutput: {result.output}")
        self.assertIn("Green time must be a non-negative integer.", result.output)

    def test_invalid_yellow_time(self) -> None:
        # Test invalid input for green time
        result = self.runner.invoke(run_traffic_light, input="0\n-1\n1\n1\nn\n")
        print(f"\noutput: {result.output}")
        self.assertIn("Yellow time must be a non-negative integer.", result.output)

    def test_invalid_red_time(self) -> None:
        result = self.runner.invoke(run_traffic_light, input="0\n0\n-1\n1\nn\n")
        self.assertIn("Red time must be a non-negative integer", result.output)

    def test_color_inputs_greater_than_zero(self) -> None:
        # Test total time must be greater than zero
        result = self.runner.invoke(run_traffic_light, input="0\n0\n0\nn\n1\n1\n1\nn\n")
        self.assertIn(
            "Total light color times must be greater than zero", result.output
        )
