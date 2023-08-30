# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
import time
from platform import python_version

from pyrogram import (Client, 
                      __version__ as pyroVer, 
                      filters)
from pyrogram.types import Message

from config import BOT_VER
from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd, ANTIPM, BROADCAST_ENABLED, BOTLOG_CHATID
from ProjectDark import CMD_HELP as modules, StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils import get_readable_time



@Client.on_message(filters.command("alive", cmd) & filters.me)
async def alive(client: Client, message: Message):
    msg = await edit_or_reply(message, "...")
    await asyncio.sleep(1)
    uptime = await get_readable_time((time.time() - StartTime))
    alive_msg = (f"""
DarkPyro-REV v{BOT_VER}

Pyrogram v{pyroVer}
Python v{python_version()}

{len(modules)} Modules Loaded
with Handler (`{cmd}`)

Broadcast = `{BROADCAST_ENABLED}`
Anti-PM = `{ANTIPM}`
Logs ID = `{BOTLOG_CHATID}`

Started since {uptime} ago.
""")
    await msg.edit(alive_msg)
