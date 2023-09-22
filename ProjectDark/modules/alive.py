# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import os
import sys
import asyncio
import time
from platform import python_version
from telegraph import upload_file
from telegraph.exceptions import TelegraphException

from pyrogram import (Client, 
                      __version__ as pyroVer, 
                      filters)
from pyrogram.types import Message

from config import BOT_VER
from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd, ANTIPM, BROADCAST_ENABLED, BOTLOG_CHATID, gvarstatus
from ProjectDark import CMD_HELP as modules, StartTime
from ProjectDark.helpers.basic import eor
from ProjectDark.helpers.tools import convert_to_image
from ProjectDark.utils import get_readable_time

def restart():
    args = [sys.executable, "-m", "ProjectDark"]
    os.execle(sys.executable, *args, os.environ)
    return

alv_logo = (
  gvarstatus("ALIVE_LOGO") or "https://telegra.ph//file/7310307cc29b4983c45d8.mp4"
)

@Client.on_message(filters.command("alive", cmd) & filters.me)
async def alive(client: Client, message: Message):
    msg = await eor(message, "...")
    await asyncio.sleep(1)
    send_mdia = client.send_video if alv_logo.endswith(".mp4") else client.send_photo
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
                msg.delete(),
                send_mdia(
                message.chat.id,
                alv_logo,
                caption=alive_msg,
                ),
    )


@Client.on_message(filters.command("setalvlogo", cmd) & filters.me)
async def setalvlogo(client: Client, message: Message):
    try:
        import ProjectDark.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    msg = await eor(message, "...")
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except TelegraphException as e:
            await msg.edit(f"**ERROR:**\n`{e}`")
            os.remove(m_d)
            return
        link = f"https://telegra.ph/{media_url[0]}"
        os.remove(m_d)
    sql.addgvar("ALIVE_LOGO", link)
    xx = f"**Successfully Customized ALIVE LOGO Become:**\n`{link}`\n\n"
    await msg.edit(xx + "**Restarting.....................................................................**", disable_web_page_preview=True)
    restart()
