# ~ported from telethon friday

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import get_text

from .help import *


@Client.on_message(filters.command("trump", cmd) & filters.me)
async def trump_tweet(client: Client, message: Message):
    text = get_text(message)
    if not text:
        await message.edit(f"Trump: What should I tweet for you?")
        return
    url = f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    r = requests.get(url=url).json()
    tweet = r["message"]
    starkxd = f"Trump has tweeted {text}"
    await message.edit(f"Trump: Wait I'm tweeting your text.")
    await client.send_photo(message.chat.id, tweet, caption=starkxd)
    await message.delete()


@Client.on_message(filters.command("tweet", cmd) & filters.me)
async def custom_tweet(client: Client, message: Message):
    text = get_text(message)
    input_str = get_text(message)
    if text:
        if ":" in text:
            stark = input_str.split(":", 1)
        else:
            await message.edit("Syntax: username:tweet-text")
            return
    if len(stark) != 2:
        await message.edit("Syntax: username:tweet-text")
        return

    starky = stark[0]
    ipman = stark[1]
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={starky}&text={ipman}"
    r = requests.get(url=url).json()
    tweet = r["message"]
    starkxd = f"{starky} has tweeted {ipman}"
    await message.edit(f"{starky}: Wait I'm tweeting your text.")
    await client.send_photo(message.chat.id, tweet, caption=starkxd)
    await message.delete()


add_command_help(
    "memes",
    [
        ["trump",
        "Make a quote by Trump."
        ],
        
        ["tweet",
        "Twitter by your values."
        ],
    ],
)
