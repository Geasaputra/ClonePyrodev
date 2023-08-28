import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from .help import add_command_help


add_command_help(
    "converter",
    [
        ["tog <reply_to_sticker/video>",
        "Convert sticker/video to gif.",
        ],
        
        ["tov <reply_to_audio/video>",
        "Convert audio/video to voice.",
        ],
        
        ["vta <reply_to_video>",
        "Convert video to audio.",
        ],
        
        ["sti <reply_to_sticker>",
        "Converting stickers to image."
        ],
        
        ["tta <text/reply>",
        f"Convert text to audio by Google. See `{cmd}help lang_id` to set language."
        ],
    ],
)

        
add_command_help(
    "lang_id",
    [
        [f"alang <lang_id>",
        "Set your voice language\n"
        "Languages Available [id: Language]:\n"
        "af: Afrikaans | ar: Arabic | cs: Czech | de: German | el: Greek | en: English | es: Spanish | fr: French | hi: Hindi | id: Indonesian | is: Icelandic | it: Italian | ja: Japanese | jw: Javanese | ko: Korean | la: Latin | my: Myanmar | ne: Nepali | nl: Dutch | pt: Portuguese | ru: Russian | su: Sundanese | sv: Swedish | th: Thai | tl: Filipino | tr: Turkish | vi: Vietname | zh-cn: Chinese (Mandarin/China) | zh-tw: Chinese (Mandarin/Taiwan)",
        ],
    ],
)


max_size = 5 * 1024 * 1024

@Client.on_message(filters.me & filters.command("tog", cmd))
async def _to_gif(client: Client, message: Message):
    await message.edit("Processing...")
    out = "./output.gif"
    mid = message.chat.id
    rep = message.reply_to_message
    if rep.sticker or rep.video:
        if (rep.video and rep.video.file_size > max_size):
            await message.edit("File size exceeds 5MB limit!")
            return
        dl = await client.download_media(rep, out)
        await message.edit("Uploading...")
        await asyncio.sleep(1)
        await client.send_animation(
            mid, 
            dl, 
            reply_to_message_id=rep.id
            )
        await message.delete()
        os.remove(out)
    else:
        await message.edit("Reply to sticker/video!")



import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio as convert_audio


@Client.on_message(filters.me & filters.command("vta", cmd))
async def _to_audio(client: Client, message: Message):
    await message.edit("Processing...")
    tmp = "./temp.mp4"
    end = "./Audio.mp3"
    mid = message.chat.id
    rep = message.reply_to_message
    art = "by DarkPyro-REV"
    title = "Audio"
    if rep.video:
        if (rep.video and rep.video.file_size > max_size):
            await message.edit("File size exceeds 5MB limit!")
            return
        dl = await client.download_media(rep, tmp)
        convert_audio(dl, end)
        await message.edit("Uploading...")
        await asyncio.sleep(1)
        await client.send_audio(
            mid, 
            end, 
            title=title,
            performer=art,
            reply_to_message_id=rep.id
            )
        await message.delete()
        os.remove(tmp)
        os.remove(end)
    else:
        await message.edit("Reply to video!")

@Client.on_message(filters.me & filters.command("tov", cmd))
async def _to_voice(client: Client, message: Message):
    await message.edit("Processing...")
    vid = "./temp.mp4"
    aud = "./output.mp3"
    mid = message.chat.id
    rep = message.reply_to_message
    if rep.video:
        if (rep.video and rep.video.file_size > max_size):
            await message.edit("File size exceeds 5MB limit!")
            return
        dl = await client.download_media(rep, vid)
        convert_audio(dl, aud)
        await message.edit("Uploading...")
        await asyncio.sleep(1)
        await client.send_voice(
            mid, 
            aud,
            reply_to_message_id=rep.id
            )
        await message.delete()
        os.remove(vid)
        os.remove(aud)
        
    if rep.audio:
        if (rep.audio and rep.audio.file_size > max_size):
            await message.edit("File size exceeds 5MB limit!")
            return
        dl = await client.download_media(rep, aud)
        await message.edit("Uploading...")
        await asyncio.sleep(1)
        await client.send_voice(
            mid, 
            dl,
            reply_to_message_id=rep.id
            )
        await message.delete()
        os.remove(aud)
        
    else:
        await message.edit("Reply to video/audio!")
