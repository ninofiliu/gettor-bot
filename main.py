import sys
import anyio
from semaphore import Bot, ChatContext
from lib import respond

bridges = []
bridges_by_username = {}

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} PHONE_NUMBER")
        exit(1)

    bot = Bot(sys.argv[1])

    @bot.handler("")
    async def handler(ctx: ChatContext) -> None:
        await ctx.message.reply(
            respond(
                ctx.message.get_body(),
                ctx.message.username,
                bridges,
                bridges_by_username,
            )
        )

    async def main():
        async with bot:
            await bot.set_profile("Example")
            await bot.start()

    anyio.run(main)
