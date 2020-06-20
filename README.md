# Python: Sonarr Client

Asynchronous Python client for Sonarr API.

## About

This package allows you to monitor a Sonarr instance.

## Installation

```bash
pip install sonarr
```

## Usage

```python
import asyncio

from sonarr import Sonarr


async def main():
    """Show example of connecting to your Sonarr instance."""
    async with Sonarr("192.168.1.100", "API_TOKEN") as sonarr:
        # basic: simple api for monitoring purposes only.
        info = await sonarr.update()
        print(info)

        calendar = await sonarr.calendar()
        print(calendar)

        commands = await sonarr.commands()
        print(commands)

        queue = await sonarr.queue()
        print(queue)

        series = await sonarr.series()
        print(series)

        wanted = await sonarr.wanted()
        print(wanted)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
