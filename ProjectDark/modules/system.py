# null
# Copyright (C) 2023 DarkPyro-REV
# Re-Code by DarkTeam - 2023
# This file is a part of < https://github.com/tracemoepy/DarkPyro-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/tracemoepy/DarkPyro-Userbot/blob/main/LICENSE/>.
# t.me/DiscussionDark & t.me/fuckdvck

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
        msg = await edit_or_reply(message, "__Restarting bot...__")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("Bot has restarted !\n\n")


add_command_help(
    "system",
    [
        ["restart", "To restart userbot."],
    ],
)
