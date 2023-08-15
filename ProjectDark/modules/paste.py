# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import os
import re

import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils.pastebin import paste

from .help import add_command_help

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@Client.on_message(filters.command("paste", cmd) & filters.me)
async def paste_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await edit_or_reply(message, f"Reply to message.")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await edit_or_reply(message, "Only text and documents are supported.")
    m = await edit_or_reply(message, "Pasting...")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("You can only paste files smaller than 40KB.")
        if not pattern.search(r.document.mime_type):
            return await m.edit("Only text files can be pasted.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste(content)
    try:
        if m.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"Result: [Link]({link})",
            )
        await m.delete()
    except Exception:
        await m.edit(f"Result: [Link]({link})")


add_command_help(
    "paste",
    [
        ["paste <reply to text/txt>",
        "Upload text to pastebin."
        ],
    ],
)
