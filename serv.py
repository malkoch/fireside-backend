import asyncio

from service import (
    camp,
    fire,
    image,
    message,
    permission,
    role,
    user
)


async def main():
    await asyncio.gather(
        asyncio.create_task(camp.run()),
        asyncio.create_task(fire.run()),
        asyncio.create_task(image.run()),
        asyncio.create_task(message.run()),
        asyncio.create_task(permission.run()),
        asyncio.create_task(role.run()),
        asyncio.create_task(user.run())
    )


asyncio.run(main())
