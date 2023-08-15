# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import sys
from os import environ, execle, remove

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import BOTLOG_CHATID, LOGGER
from ProjectDark.helpers.basic import edit_or_reply
from .help import add_command_help


@Client.on_message(filters.command("restart", cmd) & filters.me)
async def restart_bot(_, message: Message):
    try:
        msg = await edit_or_reply(message, "Restarting...")
        LOGGER(__name__).info("Restarted!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("Restarted!")
    args = [sys.executable, "-m", "ProjectDark"]
    execle(sys.executable, *args, environ)


add_command_help(
    "system",
    [
        ["restart",
        "Restart userbot."
        ],
    ],
)
