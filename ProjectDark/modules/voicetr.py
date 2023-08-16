# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
import os

from gtts import gTTS
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help

lang = "id"  # Default Language for voice


@Client.on_message(filters.me & filters.command("tts", cmd))
async def voice(client: Client, message):
    global lang
    cmd = message.command
    if len(cmd) > 1:
        v_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        v_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await edit_or_reply(
        message,
        "Reply to messages or send text arguments to convert to voice.",
        )
        return
    await client.send_chat_action(message.chat.id, enums.ChatAction.RECORD_AUDIO)
    # noinspection PyUnboundLocalVariable
    tts = gTTS(v_text, lang=lang)
    tts.save("voice.ogg")
    if message.reply_to_message:
        await asyncio.gather(
        message.delete(),
        client.send_voice(
            message.chat.id,
            voice="voice.ogg",
            reply_to_message_id=message.reply_to_message.id,
        ),
        )
    else:
        await message.delete()
        await client.send_voice(message.chat.id, voice="voice.ogg")
        os.remove("voice.ogg")


@Client.on_message(filters.me & filters.command(["voicelang"], cmd))
async def voicelang(client: Client, message: Message):
    global lang
    temp = lang
    lang = message.text.split(None, 1)[1]
    try:
        gTTS("tes", lang=lang)
    except Exception:
        await edit_or_reply(message, "Language ID invalid!")
        lang = temp
        return
    await edit_or_reply(
        message, "Language for Google Voice changed to {}".format(lang)
    )



add_command_help(
    "voice",
    [
        ["tts <text/reply>",
        "Convert text to voice by Google."
        ],
        
        [f"voicelang (lang_id)",
        "Set your voice language\n"
        "Languages Available:\n"
        "[id: Language]\n"
        "af: Afrikaans\n"
        "ar: Arabic\n"
        "cs: Czech\n"
        "de: German\n"
        "el: Greek\n"
        "en: English\n"
        "es: Spanish\n"
        "fr: French\n"
        "hi: Hindi\n"
        "id: Indonesian\n"
        "is: Icelandic\n"
        "it: Italian\n"
        "ja: Japanese\n"
        "jw: Javanese\n"
        "ko: Korean\n"
        "la: Latin\n"
        "my: Myanmar\n"
        "ne: Nepali\n"
        "nl: Dutch\n"
        "pt: Portuguese\n"
        "ru: Russian\n"
        "su: Sundanese\n"
        "sv: Swedish\n"
        "th: Thai\n"
        "tl: Filipino\n"
        "tr: Turkish\n"
        "vi: Vietname\n"
        "zh-cn: Chinese (Mandarin/China)\n"
        "zh-tw: Chinese (Mandarin/Taiwan)",
        ],
    ],
)
