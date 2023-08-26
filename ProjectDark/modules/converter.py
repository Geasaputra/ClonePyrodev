import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from .help import add_command_help


add_command_help(
    "converter",
    [
        ["stg <reply_to_sticker>",
        "Convert sticker to gif.",
        ],
        
        ["vta <reply_to_video>",
        "Convert video to audio.",
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



@Client.on_message(filters.me & filters.command("stg", cmd))
async def _to_gif(client: Client, message: Message):
    await message.edit("Processing...")
    out = "./output.mp4"
    mid = message.chat.id
    rep = message.reply_to_message
    if rep.sticker:
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
        await message.edit("Reply to sticker!")



import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio as convert_audio


@Client.on_message(filters.me & filters.command("vta", cmd))
async def _to_audio(client: Client, message: Message):
    await message.edit("Processing...")
    tmp = "./temp.mp4"
    end = "./DarkPyro_Extractor.mp3"
    mid = message.chat.id
    rep = message.reply_to_message
    if rep.video:
        dl = await client.download_media(rep, tmp)
        convert_audio(dl, end)
        await message.edit("Uploading...")
        await asyncio.sleep(1)
        await client.send_audio(
            mid, 
            end, 
            reply_to_message_id=rep.id
            )
        await message.delete()
        os.remove(tmp)
        os.remove(end)
    else:
        await message.edit("Reply to video!")
