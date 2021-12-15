import asyncio

from sonarr import Sonarr


async def main():
    """Show example of connecting to your Sonarr instance."""
    async with Sonarr("10.1.10.10", "749e77d241704f29a98f65c874de964a") as sonarr:
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
