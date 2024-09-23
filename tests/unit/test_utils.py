from unittest import IsolatedAsyncioTestCase

from traffic_light.container import ContainerSingleton


class TrafficLightTestCaseWithContainerSingleton(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        """Ensure we're always using an isolated Container object"""
        self.container = ContainerSingleton.reset()
