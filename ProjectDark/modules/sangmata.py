# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import *
from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import *

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils import extract_user

from .help import add_command_help


@Client.on_message(filters.command("sg", cmd) & filters.me)
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await edit_or_reply(message, "Processing...")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"Specify a valid user!")
    bot = "SangMata_BOT"
    try:
        await client.send_message(bot, f"{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"{user.id}")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot, query="available", limit=1):
        if not stalk:
            await message.edit_text("No history!")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()

    async for stalk in client.search_messages(bot, query=["names", "usernames"], limit=5):
        if not stalk:
            return
        elif stalk:
            await message.reply(stalk.text)
            await stalk.delete()


add_command_help(
    "sangmata",
    [
        ["sg <reply/userid/username>",
        "Check history name/username of users.",
        ],
    ],
)
