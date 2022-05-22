import sqlite3
import sys
from sqlite3 import connect

import anyio
from semaphore import Bot, ChatContext

from lib import respond

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} PHONE_NUMBER")
        exit(1)

    con = connect("db.db")
    con.row_factory = sqlite3.Row

    bot = Bot(sys.argv[1])

    @bot.handler("")
    async def handler(ctx: ChatContext) -> None:
        text = ctx.message.get_body()
        username = ctx.message.source.number
        response = respond(con, text, username)
        print(f"{username} <\n{text}")
        print(f"{sys.argv[1]} >\n{response}")
        await ctx.message.reply(response)

    async def main():
        async with bot:
            await bot.set_profile("GettorBot")
            await bot.start()

    anyio.run(main)
