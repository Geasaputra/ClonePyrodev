# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import os
import sys
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message

from ProjectDark import LOGGER
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.tools import get_arg
from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd, BOTLOG_CHATID, BROADCAST_ENABLED, addgvar, gvarstatus
from .help import add_command_help



@Client.on_message(filters.command("restart", cmd) & filters.me)
async def restart_bot(client: Client, message: Message):
    try:
        msg = await edit_or_reply(message, "Restarting...")
        LOGGER(__name__).info("Restarting...")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    
    try:
        logs_file = "logs.txt"
        os.remove(logs_file)
    except Exception as e:
        LOGGER(__name__).info(f"{e}")
    await msg.edit_text("Restarted!")
    args = [sys.executable, "-m", "ProjectDark"]
    subprocess.Popen(args, env=os.environ)


@Client.on_message(filters.command("handler", cmd) & filters.me)
async def set_handler(client: Client, message: Message):
    handler = get_arg(message)
    if not handler:
        return await edit_or_reply(message, f"Set with `{cmd}handler x` or etc.")
    else:
        addgvar("CMD_HANDLER", handler)
        await message.edit(f"Handler changed to {handler}\nRestart userbot to take effect.")
        


@Client.on_message(filters.command("setlogs", cmd) & filters.me)
async def set_logs(client: Client, message: Message):
    logger = get_arg(message)
    logger_status = gvarstatus("BOTLOG_CHATID")
    logger_status = "Default" if logger_status == "me" else "Group"
    if not logger:
        return await edit_or_reply(message, f"Currently logs chat_id is {logger_status}")
    if not (logger.startswith("-100") or logger.startswith("me")):
        return await edit_or_reply(message, "Invalid!")
    else:
        addgvar("BOTLOG_CHATID", logger)
        await message.edit(f"Logs chat_id changed to {logger}\nRestart userbot to take effect.")
        


@Client.on_message(filters.command("broadcast", cmd) & filters.me)
async def set_broadcast(client: Client, message: Message):
    broadcast = get_arg(message)
    broadcast_status = gvarstatus("BROADCAST_ENABLED")
    if not broadcast:
        return await edit_or_reply(message, f"Currently broadcast is {broadcast_status}")
    if broadcast not in ["on", "off"]:
        return await edit_or_reply(message, "Invalid!")
    else:
        addgvar("BROADCAST_ENABLED", broadcast)
        await message.edit(f"Broadcast changed to {broadcast}\nRestart userbot to take effect.")
        


@Client.on_message(filters.command("logs", cmd) & filters.me)
async def send_logs(client: Client, message: Message):
    try:
        send = await message.edit("Sending...")

        if not os.path.exists("logs.txt"):
            await send.edit("No logs available!")
            return

        await client.send_document(
            BOTLOG_CHATID,
            "logs.txt",
            reply_to_message_id=message.id,
            )
        os.remove("logs.txt")

        await send.edit("Your logs has been sent to logs chat_id.")

    except Exception as e:
        await send.edit(e)
    


@Client.on_message(filters.command("killme", cmd) & filters.me)
async def logout(client: Client, message: Message):
    conf = get_arg(message)
    if "True" not in conf:
        await edit_or_reply(message, f"Use `{cmd}killme True` to kill your userbot session.")
    else:
        await edit_or_reply(message, "Userbot's session has been logged out!")
        await client.log_out()
    
    
add_command_help(
    "system",
    [
        ["handler",
        "Set your prefix/cmd/handler.",
        ],

        ["restart",
        "Restart userbot.",
        ],

        ["update",
        "Check update.",
        ],

        ["setlogs",
        "Set your userbot logs chat_id.",
        ],
        
        ["broadcast",
        "Active/deactive broadcast module.",
        ],

        ["logs",
        "Get usetbot logs.",
        ],
        
        ["killme",
        "Kill userbot (logged out userbot's session).",
        ],
    ],
)
