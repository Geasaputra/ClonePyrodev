# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.tools import get_arg

from .help import add_command_help

spam_chats = []


@Client.on_message(filters.command("tagall", cmd) & filters.me)
async def tagall(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    string = ""
    limit = 1
    gcm = client.get_chat_members(chat_id)
    async for member in gcm:
        tag = member.user.username
        if limit <= 15:
            string += f"@{tag}\n" if tag != None else f"{member.user.mention}\n"
            limit += 1
        else:
            await client.send_message(chat_id, text=string)
            limit = 1
            string = ""
            await asyncio.sleep(1)



add_command_help(
    "tagall",
    [
        ["tagall [text/reply to chat]",
        "Tag everyone.",
        ],
    ],
)
