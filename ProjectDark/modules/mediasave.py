import os

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOTLOG_CHATID as log
from .help import add_command_help


@Client.on_message(filters.command(["wow", "wah"], "") & filters.me)
async def scrape(client: Client, message: Message):
    rep = message.reply_to_message
    if rep:
        if rep.photo or rep.video:
            await message.delete()
            mtype = "photo" if rep.photo else "video"
            copy = await client.download_media(rep)
            await getattr(client, f"send_{mtype}")(log, copy, rep.caption)
            os.remove(copy)

add_command_help(
  "mediasave",
  [
    ["wah or wow w/o cmd",
    "Save photo with timer to your saved message."
    ],
  ],
)
