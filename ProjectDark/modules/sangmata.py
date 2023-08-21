# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import *
from pyrogram.raw import functions

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils import extract_user

@Client.on_message(filters.command("sg", cmd) & filters.me)
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    msg = await edit_or_reply(message, "Processing...")
    if not args:
        await msg.edit("Specify a valid user or reply to user's message!")
    else:
        target = await client.get_users(args)
    
    bot = "SangMata_BOT"    
    try:
        send = await client.send_message(bot, target.id)
        await client.delete
    except YouBlockedUser:
        return await msg.edit("Unblock @SangMata_BOT!")
        
    async for stalk in client.search_messages(bot, query="History", limit=1):
        await msg.edit(stalk.text)
        await asyncio.sleep(3)
        bots = await client.resolve_peer(bot)
        await client.send(
            functions.messages.DeleteHistory(peer=bots, max_id=0, revoke=True)
            )
