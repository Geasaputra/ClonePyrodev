import asyncio
import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.tools import get_arg

from .help import add_command_help


@Client.on_message(filters.command("gcast", cmd) & filters.me)
async def gcast_cmd(client, message):
    if message.reply_to_message or get_arg(message):
        kang = await message.reply("Broadcasting message...")
    else:
        return await message.edit("Give me a text or reply to chat")
    done = 0
    error = 0
    user_id = client.me.id
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg(message):
                msg = get_arg(message)
            chat = dialog.chat.id
            try:
                if message.reply_to_message:
                    await msg.copy(chat)
                elif get_arg(message):
                    await client.send_message(chat, msg)
                done += 1
                await asyncio.sleep(0.3)
            except Exception:
                error += 1
    await kang.edit(
        f"#Group_Broadcast\n\n  • Success: {done}\n  • Failed: {error}")

@Client.on_message(filters.command("gucast", cmd) & filters.me)
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        text = await message.reply_text("Broadcasting message...")
    else:
        return await message.edit_text("Give me a text or reply to chat")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            try:
                if message.reply_to_message:
                    await msg.copy(chat)
                elif get_arg:
                    await client.send_message(chat, msg)
                done += 1
                await asyncio.sleep(0.3)
            except Exception:
                error += 1
                await asyncio.sleep(0.3)
    await text.edit_text(
        f"#User_Broadcast\n\n  • Success: {done}\n  • Failed: {error}")

@Client.on_message(filters.command("gcastfwd", cmd) & filters.me)
async def gcast_fwd(client, message):
    if not message.reply_to_message and not get_arg(message):
        return await message.edit("Reply to the message or media to be forwarded")

    kang = await message.reply("Broadcasting forwarded chat...")

    done = 0
    error = 0
    user_id = client.me.id
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            try:
                if message.reply_to_message:
                    await message.reply_to_message.forward(chat.id)
                elif get_arg(message):
                    await client.send_message(chat.id, get_arg(message))
                done += 1
                await asyncio.sleep(0.3)
            except Exception:
                error += 1

    await kang.edit(
        f"#Forward_Broadcast\n\n  • Success: {done}\n  • Failed: {error}")

add_command_help(
    "broadcast",
    [
        ["gcast <text>",
        "Broadcast a message to group!",
        ],
        
        ["gucast <text>",
        "Broadcast a message to mutual contact!",
        ],
        
        ["gcastfwd <reply to chat/media>",
        "Broadcast a forwaded message!",
        ],
    ],
)
