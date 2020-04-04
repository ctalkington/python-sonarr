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
        info = sonarr.update()
        print(info)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
