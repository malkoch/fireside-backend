import asyncio

from service import (
    camp,
    fire,
    message
)


async def main():
    await asyncio.gather(
        asyncio.create_task(camp.run()),
        asyncio.create_task(fire.run()),
        asyncio.create_task(message.run())
    )


asyncio.run(main())
