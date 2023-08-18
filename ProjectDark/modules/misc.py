# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
import os

from pyrogram import Client, enums, filters, raw
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import *
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.PyroHelpers import ReplyCheck
from ProjectDark.helpers.tools import get_arg

from .help import *


@Client.on_message(filters.command("limit", cmd) & filters.me)
async def spamban(client: Client, m: Message):
    await client.unblock_user("SpamBot")
    response = await client.send(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    wait_msg = await edit_or_reply(m, "Checking...")
    await asyncio.sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await wait_msg.edit_text(f"~ {status.text}")


@Client.on_message(filters.command("webshot", cmd) & filters.me)
async def webshot(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Taking...")
    try:
        user_link = message.command[1]
        try:
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"Screenshot: {user_link}",
            )
        except Exception as dontload:
            await message.edit(f"Error! {dontload}\nTrying again create screenshot...")
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"Screenshot: {user_link}",
            )
        await Dark.delete()
    except Exception as error:
        await Dark.delete()
        await client.send_message(
            message.chat.id, f"{error}"
            )


@Client.on_message(filters.command("type", cmd) & filters.me)
async def types(client: Client, message: Message):
    orig_text = message.text.split(cmd + "type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "..."
    while tbp != orig_text:
        await message.edit(str(tbp + typing_symbol))
        await asyncio.sleep(0.10)
        tbp = tbp + text[0]
        text = text[1:]
        await message.edit(str(tbp))
        await asyncio.sleep(0.10)


@Client.on_message(filters.command("dm", cmd) & filters.me)
async def deem(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Sending...")
    quantity = 1
    inp = message.text.split(None, 2)[1]
    user = await client.get_chat(inp)
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id
        for _ in range(quantity):
            await Dark.edit("Successfully sent!")
            await client.send_message(
                user.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await client.send_message(user.id, spam_text)
        await Dark.edit("Successfully sent!")
        await asyncio.sleep(0.15)


@Client.on_message(filters.command("mdl", cmd) & filters.me)
async def sosmed(client: Client, message: Message):
    Dark = await message.edit("Downloading...")
    link = get_arg(message)
    bot = "thisvidbot"
    if link:
        try:
            xnxx = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xnxx.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xnxx.delete()
    async for sosmed in client.search_messages(
        bot, filter=enums.MessagesFilter.VIDEO, limit=1
    ):
        await asyncio.gather(
            Dark.delete(),
            client.send_video(
                message.chat.id,
                sosmed.video.file_id,
                caption=f"Uploaded by {client.me.mention}",
                reply_to_message_id=ReplyCheck(message),
            ),
        )
        await client.delete_messages(bot, 2)


add_command_help(
    "misc",
    [
        ["limit",
        "Check Limit telegram from @SpamBot."
        ],
        
        ["dm @username <text>",
        "Send chat using userbot.",
        ],

        ["type",
        "Typing text by text.",
        ],
    ],
)


add_command_help(
    "webshot",
    [
        [f"webshot <link>",
        "To take screenshot of a web page.",
        ],
    ],
)


add_command_help(
    "mediadl",
    [
        [f"mdl <link>",
        "Download media from Facebook/Tiktok/Instagram/Twitter/YouTube.",
        ],
    ],
)
