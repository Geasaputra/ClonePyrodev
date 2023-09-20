# imported from dragon-fork

import os

from pyrogram import Client, filters
from pyrogram.types import Message

from .help import add_command_help

@Client.on_message(filters.command("copy", prefix) & filters.me)
async def _copy(client: Client, message: Message):
    if len(message.command) == 1:
        return await message.edit(
            "Send command along with Telegram link post!")
    await message.edit("Processing...")
    if "https://t.me/" in message.command[1]:
        datas = message.text.split("/")
        msgid = int(datas[-1].split("?")[0])
        
        if "https://t.me/c/" in message.command[1]:
            chatid = int("-100" + datas[-2])
            try: 
               await download(
                    client,
                    message,
                    chatid,
                    msgid,
                )
            except Exception as e:
                await message.edit(format_exc(e))
        else:
            username = datas[-2]
            msg  = await client.get_messages(
                username, msgid
            )
            try: 
               await download(
                    client,
                    message,
                    username,
                    msgid,
                )
            except Exception as e:
                await message.edit(format_exc(e))
    else:
        return await message.edit("Link invalid!")


add_command_help(
  "copy",
  [
    ["copy [link post]",
    "Save post from channel or group private."
    ],
  ],
)
