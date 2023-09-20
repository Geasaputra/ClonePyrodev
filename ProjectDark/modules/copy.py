# imported from dragon-fork

import os

from pyrogram import Client, filters
from pyrogram.types import Message

from .help import add_command_help


async def download(
    client,
    message,
    chatid,
    msgid
):
    msg = await client.get_messages(chatid, msgid)
    if "text" in str(msg):
        await client.send_message(
            message.chat.id,
            msg.text,
        )
        return await message.delete()
    file = await client.download_media(msg)
    if "Document" in str(msg):
        await client.send_document(
            message.chat.id,
            file,
            caption=msg.caption,
        )
    elif "Video" in str(msg):
        await client.send_video(
            message.chat.id,
            file,
            duration=msg.video.duration,
            width=msg.video.width,
            height=msg.video.height,
            caption=msg.caption,
        )
    elif "Animation" in str(msg):
        await client.send_animation(
            message.chat.id,
            file,
        )
    elif "Sticker" in str(msg):
        await client.send_sticker(
            message.chat.id,
            file,
        )
    elif "Voice" in str(msg):
        await client.send_voice(
            message.chat.id,
            file,
            caption=msg.caption,
        )
    elif "Audio" in str(msg):
        await client.send_audio(
            message.chat.id,
            file,
            caption=msg.caption,
        )   
    elif "Photo" in str(msg):
        await client.send_photo(
            message.chat.id,
            file,
            caption=msg.caption,
        )
    os.remove(file)
    await message.delete()


@Client.on_message(filters.command("copy", cmd) & filters.me)
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
                await message.edit(f"{str(e)}")
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
                await message.edit(f"{str(e)}")
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
