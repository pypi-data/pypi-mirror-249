# reswarm-py

## About

Makes publishing data to a Record Evolution Datapod incredibly easy!

## Usage

```python
import asyncio
from reswarm import Reswarm

# create a reswarm instance, which auto connects to the Record Evolution Platform
# the reswarm instance handles authentication and reconnects when connection is lost
rw = Reswarm()

async def main():
    while True:
        # publish an event (if connection is not established the publish is skipped)
        publication = await rw.publish("test.publish.com", {"temperature": 20})
        print(publication)
        await asyncio.sleep(3)


if __name__ == "__main__":
    # run the main coroutine
    asyncio.get_event_loop().create_task(main())
    # run the reswarm component
    rw.run()
```

## Options

The `Reswarm` `__init__` function can be configured with the following options:

```
{
    serial_number: string;
}
```

**serial_number**: Used to set the serial_number of the device if the `DEVICE_SERIAL_NUMBER` environment variable does not exist. It can also be used if the user wishes to authenticate as another device.

## Advanced Usage

If you need more control, e.g. acting on lifecycle events (`onJoin`, `onLeave`) take a look at
the [examples](./examples/) folder.
