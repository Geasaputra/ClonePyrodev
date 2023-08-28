# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
import os
import time
from platform import python_version

from pyrogram import (Client, 
                      __version__ as pyroVer, 
                      filters)
from pyrogram.types import Message

from config import BOT_VER
from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from ProjectDark import CMD_HELP, StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.PyroHelpers import ReplyCheck
from ProjectDark.helpers.tools import convert_to_image
from ProjectDark.utils import get_readable_time
from ProjectDark.utils.misc import restart


modules = CMD_HELP


@Client.on_message(filters.command("alive", cmd) & filters.me)
async def alive(client: Client, message: Message):
    msg = await edit_or_reply(message, "...")
    await asyncio.sleep(1)
    uptime = await get_readable_time((time.time() - StartTime))
    alive_msg = (f"""
DarkPyro-REV v{BOT_VER}

{len(modules)} Modules Loaded
with Handler (`{cmd}`)

Pyrogram v{pyroVer}
Python v{python_version()}

Started since {uptime} ago.
""")
    try:
        await asyncio.gather(
            msg.delete(),
            msg.send(
                message.chat.id,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await msg.edit(alive_msg, disable_web_page_preview=True)
