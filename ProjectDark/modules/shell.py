# Part of Dragon-Userbot - 2022
# Kang by DarkPyro - 2023

from subprocess import Popen, PIPE, TimeoutExpired
import os
from time import perf_counter

from pyrogram import Client, filters
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd

from .help import add_command_help


@Client.on_message(filters.me & filters.command("sh", cmd))
async def shell(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit("Specify the command in message text!")
    cmd_text = message.text.split(maxsplit=1)[1]
    cmd_obj = Popen(
        cmd_text,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )

    char = "DarkPyro#" if os.getuid() == 0 else "DarkPyro$"
    text = f"{char} <code>{cmd_text}</code>\n\n"

    await message.edit("Running...")
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "Timeout expired!"
    else:
        stop_time = perf_counter()
        if len(stdout) > 4096:
            await message.edit(
                "Oversize, sending file...")
            file = open("output.txt", "w+")
            file.write(stdout)
            file.close()
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,)
            os.remove("output.txt")
        else:
            text += f"<code>{stdout}</code>"
        if stderr:
            text += f"<code>{stderr}</code>"
        text += f"\n\nCompleted in {round(stop_time - start_time, 5)}s"
    await message.edit(text)
    cmd_obj.kill()
    

add_command_help(
    "shell",
    [
        [f"sh",
        "Run bash.",
        ],
    ],
)