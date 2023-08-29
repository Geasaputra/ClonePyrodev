# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import importlib

from pyrogram import idle
from uvloop import install

from config import BOT_VER
from ProjectDark.helpers.SQL.globals import CMD_HANDLER, BOTLOG_CHATID
from ProjectDark import LOGGER, LOOP, aiosession, bot
from ProjectDark.modules import ALL_MODULES

MSG_ON = """
**DarkPyro-REV Started!**
Version: `{}`
Handler: `{}`
"""


async def main():
    for all_module in ALL_MODULES:
        importlib.import_module(f"ProjectDark.modules.{all_module}")
        try:
            await bot.start()
            bot.me = await bot.get_me()
            try:
                await bot.send_message(
                    BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER)
                )
            except BaseException:
                pass
            LOGGER("ProjectDark").info(
                f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
            )
        except Exception:
            pass
            #LOGGER("main").warning(a)
    LOGGER("ProjectDark").info(f"Darkpyro-UserBot v{BOT_VER} [Activated!]")
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("ProjectDark").info("Starting Darkpyro-UserBot")
    install()
    LOOP.run_until_complete(main())
