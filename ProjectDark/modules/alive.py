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
from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd, ANTIPM, BROADCAST_ENABLED, BOTLOG_CHATID, gvarstatus
from ProjectDark import CMD_HELP as modules, StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils import get_readable_time


photo = "https://telegra.ph//file/c0b5e27763fa5a9f70bd1.jpg"

@Client.on_message(filters.command("alive", cmd) & filters.me)
async def alive(client: Client, message: Message):
    #msg = await edit_or_reply(message, "...")
    await asyncio.sleep(1)
    uptime = await get_readable_time((time.time() - StartTime))
    logs = gvarstatus("BOTLOG_CHATID")
    logs = "Default" if logs == "me" else "Group"
    alive_msg = (f"""
DarkPyro-REV v{BOT_VER}

Pyrogram v{pyroVer}
Python v{python_version()}

{len(modules)} Modules Loaded
with Handler (`{cmd}`)

Broadcast = {BROADCAST_ENABLED}
Anti-PM = {ANTIPM}
Logs ID = {logs}

Started since {uptime} ago.
""")
    await asyncio.gather(
                message.delete(),
                client.send_photo(chat_id=message.chat.id, photo=photo, caption=alive_msg
                                 ),
    )
