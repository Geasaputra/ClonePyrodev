# Part of PyroMan - 2022
# Kang by DarkPyro - 2023


import asyncio

from pyrogram import Client, filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils import extract_user

@Client.on_message(filters.command("sg", cmd) & filters.me)
async def sg(client: Client, message: Message):
    bot  = "SangMata_bot"
    args = await extract_user(message)
    msg  = await edit_or_reply(message, "Processing...")
    if not args:
        await msg.edit("Specify a valid user or reply to user's message!")
    else:
        target = await client.get_users(args)
    
        try:
            send = await client.send_message(bot, target.id)
            await asyncio.sleep(3)
            await send.delete()
        except YouBlockedUser:
            await msg.edit(f"Unblock @{bot}, to use this command.")
            return

        async for history in client.get_chat_history(bot, limit=1):
            await msg.edit(history.text)
            await asyncio.sleep(5)
            await history.delete()
