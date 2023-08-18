# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import sys
from os import environ, execle, remove

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import BOTLOG_CHATID, LOGGER
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.tools import get_arg
from .help import add_command_help


@Client.on_message(filters.command("restart", cmd) & filters.me)
async def restart_bot(client: Client, message: Message):
    try:
        msg = await edit_or_reply(message, "Restarting...")
        LOGGER(__name__).info("Restarted!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    
    try:
        logs_file = "logs.txt"
        os.remove(logs_file)
    except Exception as e:
        LOGGER(__name__).info(f"Error while deleting logs.txt: {e}")
        
    await msg.edit_text("Restarted!")
    args = [sys.executable, "-m", "ProjectDark"]
    execle(sys.executable, *args, environ)


@Client.on_message(filters.command("logs", cmd) & filters.me)
async def send_logs(client: Client, message: Message):
    try:
        send = await message.edit("Send logs...")

        if not os.path.exists("logs.txt"):
            await send.edit("No logs available!")
            return

        await client.send_document(
            message.chat.id,
            "logs.txt",
            reply_to_message_id=message.id,
        )

        await message.delete()
        await send.delete()

    except Exception as e:
        await send.edit(f"{e}")
    


@Client.on_message(filters.command("killme", cmd) & filters.me)
async def logout(client: Client, message: Message):
    conf = get_arg(message)
    if "True" not in conf:
        await edit_or_reply(message, f"Type `{cmd}killme True` to kill your userbot session.")
    else:
        await edit_or_reply(message, "Session has been logged out!")
        await client.log_out()
    
    
add_command_help(
    "system",
    [
        ["alive",
        "Just for fun.",
        ],
        
        ["repo",
        "Display the repo of this userbot.",
        ],
        
        ["creator",
        "Show the creator of this userbot.",
        ],
        
        ["id",
        "Send id of what you replied to.",
        ],
        
        ["uptime",
        "Check bot's current uptime.",
        ],
        
        ["restart",
        "Restart userbot.",
        ],

        ["update",
        "Check update.",
        ],
        
        ["update deploy",
        "Update and re-deploy.",
        ],
        
        ["logs",
        "Get usetbot logs.",
        ],
        
        ["killme True",
        "Kill userbot (log_out session).",
        ],
    ],
)
