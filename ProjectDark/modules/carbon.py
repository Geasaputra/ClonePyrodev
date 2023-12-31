# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from ProjectDark import aiosession
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.PyroHelpers import ReplyCheck

from .help import add_command_help


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@Client.on_message(filters.command("carbon", cmd) & filters.me)
async def carbon_func(client: Client, message: Message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    Dark = await edit_or_reply(message, "Processing...")
    carbon = await make_carbon(text)
    await Dark.edit("Uploading...")
    await asyncio.gather(
        Dark.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"Carbonised by {client.me.mention}",
            reply_to_message_id=ReplyCheck(message),
        ),
    )
    carbon.close()


add_command_help(
    "carbon",
    [
        ["carbon <text/reply to text>",
        "Carbonised text."
        ],
    ],
)
