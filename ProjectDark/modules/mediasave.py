# Part of Dragon-Userbot - 2022
# Kang by DarkPyro - 2023

import os

from pyrogram import Client, filters
from pyrogram.types import Message

from .help import add_command_help


@Client.on_message(filters.command(["wow", "wah"], "") & filters.me)
async def scrape(client: Client, message: Message):
    rep = message.reply_to_message
    cap = rep.caption or None
    
    if rep.photo:
        copy = await client.download_media(rep)
        await message.delete()
        await client.send_photo("me", copy, cap)
        os.remove(copy)

    elif rep.video:
        copy = await client.download_media(rep)
        await message.delete()
        await client.send_video("me", copy, cap)
        os.remove(copy)
        return


add_command_help(
  "mediasave",
  [
    ["wah or wow w/o cmd",
    "Save photo with timer to your saved message."
    ],
  ],
)
