import sys
import anyio
from semaphore import Bot, ChatContext

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} PHONE_NUMBER")
    exit(1)

bot = Bot(sys.argv[1])


@bot.handler("")
async def handler(ctx: ChatContext) -> None:
    print(ctx.message.get_body())
    text = ctx.message.get_body()
    print(f"received: {text}")
    prefix = "scream this: "
    if text.startswith(prefix):
        await ctx.message.reply(text[len(prefix) :].upper())


async def main():
    async with bot:
        await bot.set_profile("Example")
        await bot.start()


anyio.run(main)
