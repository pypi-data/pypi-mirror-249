import os
from typing import Optional
from autobahn.asyncio.component import Component, run
from autobahn.wamp.interfaces import ISession
from autobahn.wamp.types import PublishOptions
from autobahn.wamp.request import Publication

from reswarm.AutobahnConnection import getSerialNumber, create_application_component


class Reswarm:
    """Convenience class for easy to use message publishing to the RE platform.

    Example:

        rw = Reswarm()

        async def main():
            while True:
                publication = await rw.publish("test.publish.pw", 1, "two", 3, foo="bar")
                print(publication)
                await asyncio.sleep(3)


        if __name__ == "__main__":
            asyncio.get_event_loop().create_task(main())
            rw.run()
    """

    def __init__(self, serial_number: str = None, mainFunc=None) -> None:
        """Creates Reswarm Instance

        Args:
            serial_number (str, optional): serial_number of device.
            Defaults to None, in which case the environment variable DEVICE_SERIAL_NUMBER is used.
        """
        self._serial_number = getSerialNumber(serial_number)
        self._component = create_application_component(serial_number)
        self._session: ISession = None
        self.mainFunc = mainFunc

        @self._component.on_join
        async def onJoin(session, details):
            print("component joined")
            self._session = session
            if self.mainFunc: 
                await self.mainFunc()

        @self._component.on_disconnect
        def onDisconnect(*args, **kwargs):
            print("component disconnected")
            self._session = None

        @self._component.on_leave
        def onLeave(*args, **kwargs):
            print("component left")
            self._session = None

    @property
    def component(self) -> Component:
        """The Autobahn Component

        Returns:
            Component
        """
        return self._component

    @property
    def session(self) -> Optional[ISession]:
        """The Autobahn Session

        Returns:
            Optional[ISession]
        """
        return self._session

    async def publish(self, topic: str, *args, **kwargs) -> Optional[Publication]:
        """Publishes to the RE Platform Message Router

        Args:
            topic (str): The URI of the topic to publish to, e.g. "com.myapp.mytopic1"

        Returns:
            Optional[Publication]: Object representing a publication
            (feedback from publishing an event when doing an acknowledged publish)
        """
        device_name = os.environ.get("DEVICE_NAME")

        extra = {
            "DEVICE_SERIAL_NUMBER": self._serial_number,
            "options": PublishOptions(acknowledge=True),
        }

        if device_name:
            extra["DEVICE_NAME"] = device_name

        if self._session is not None:
            pub = await self._session.publish(topic, *args, **kwargs, **extra)
            return pub
        else:
            print("cannot publish, not connected")

    async def publish_to_table(
        self, tablename: str, *args, **kwargs
    ) -> Optional[Publication]:
        """Publishes Data to a Table in the RE Platform

        Args:
            tablename (str): The table name of the table to publish to, e.g. "sensordata"

        Returns:
            Optional[Publication]: Object representing a publication
            (feedback from publishing an event when doing an acknowledged publish)
        """

        if not tablename:
            raise Exception("Tablename must not be None or empty string!")

        swarm_key = os.environ.get("SWARM_KEY")
        app_key = os.environ.get("APP_KEY")
        env_value = os.environ.get("ENV")

        if swarm_key is None:
            raise Exception("Environment variable SWARM_KEY not set!")

        if app_key is None:
            raise Exception("Environment variable APP_KEY not set!")

        if env_value is None:
            raise Exception("Environment variable ENV not set!")

        if not env_value in ["DEV", "PROD"]:
            raise Exception("Environment variable ENV must be 'PROD' or 'DEV'!")

        if env_value == "PROD":
            topic = f"{swarm_key}.{app_key}.{tablename}"
        else:
            topic = f"dev.{swarm_key}.{app_key}.{tablename}"

        pub = await self.publish(topic, *args, **kwargs)
        return pub

    def run(self):
        """Runs the Component in the asyncio event loop."""
        run([self._component])
