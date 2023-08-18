# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import time

from datetime import datetime

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils.tools import get_readable_time
from .help import add_command_help


class network:
    NearestDC = """
Country: {}
Nearest DC: {}
DC: {}
"""


@Client.on_message(filters.command("devil", "") & filters.me & filters.chat(-1001938021731))
async def _react(client: Client, message: Message):
    await message.react("😈")


@Client.on_message(filters.command("dc", cmd) & filters.me)
async def nearest_dc(client: Client, message: Message):
    dc = await client.send(functions.help.GetNearestDc())
    await edit_or_reply(
        message, network.NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc)
    )


@Client.on_message(filters.command("ping", cmd) & filters.me)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    msg = await edit_or_reply(message, "Checking...")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await msg.edit(
        f"Latency Result: %sms\n"
        f"Started since {uptime} ago" % (duration)
    )


add_command_help(
    "network",
    [
        ["dc",
        "Get DC info."
        ],
        
        ["ping",
        "Latency checking."
        ],
    ],
)

