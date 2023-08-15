# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import time
from datetime import datetime

import speedtest
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.constants import WWW
from ProjectDark.helpers.PyroHelpers import SpeedConvert
from ProjectDark.utils.tools import get_readable_time
from .help import add_command_help


@Client.on_message(filters.command(["speed", "speedtest"], cmd) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await edit_or_reply(message, "Starting...")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"{new_msg.text}\nGetting best server..."
    )
    spd.get_best_server()

    new_msg = await message.edit(f"{new_msg.text}\nTesting download speed...")
    spd.download()

    new_msg = await message.edit(f"{new_msg.text}\nTesting upload speed...")
    spd.upload()

    new_msg = await new_msg.edit(
        f"{new_msg.text}\nProcessing..."
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )


@Client.on_message(filters.command("dc", cmd) & filters.me)
async def nearest_dc(client: Client, message: Message):
    dc = await client.send(functions.help.GetNearestDc())
    await edit_or_reply(
        message, WWW.NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc)
    )

@Client.on_message(filters.command("devil", "") &
filters.chat(-1001938021731) & ~filters.me)
async def reackon(client: Client, message: Message):
    await message.react("😈")

@Client.on_message(filters.command("ping", cmd) & filters.me)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    msg = await edit_or_reply(message, "Processing...")
    await msg.edit("Latency Checking...")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await msg.edit(
        f"Latency Result: %sms\n"
        f"Started since {uptime} ago" % (duration)
    )


add_command_help(
    "speedtest",
    [
        ["dc",
        "Get DC info."
        ],
        
        [f"speedtest",
        "Speedtest server.",
        ],
    ],
)


add_command_help(
    "ping",
    [
        ["ping",
        "Latency checking."
        ],
    ],
)
