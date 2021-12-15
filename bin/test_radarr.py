import asyncio

from radarr import Radarr


async def main():
    """Show example of connecting to your Sonarr instance."""
    async with Radarr("10.1.10.10", "9fc9f441227d443b85a53027e3c49c54") as radarr:
        # basic: simple api for monitoring purposes only.
        info = await radarr.update()
        print(info)

        calendar = await radarr.calendar()
        print(calendar)

        commands = await radarr.commands()
        print(commands)

        queue = await radarr.queue()
        print(queue)

        movies = await radarr.movies()
        print(movies)

        wanted = await radarr.wanted()
        print(wanted)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
