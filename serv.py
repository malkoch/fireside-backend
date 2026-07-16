import asyncio

from service import (
    campfire,
    fellowship,
    message
)


async def main():
    await asyncio.gather(
        asyncio.create_task(campfire.run()),
        asyncio.create_task(fellowship.run()),
        asyncio.create_task(message.run())
    )


asyncio.run(main())
