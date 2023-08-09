# null
# Copyright (C) 2023 DarkPyro-REV
# Re-Code by DarkTeam - 2023
# This file is a part of < https://github.com/tracemoepy/DarkPyro-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/tracemoepy/DarkPyro-Userbot/blob/main/LICENSE/>.
# t.me/DiscussionDark & t.me/fuckdvck

from gpytranslate import Translator
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.me & filters.command(["tr", "trt", "translate"], cmd))
async def translate(client: Client, message: Message):
    trl = Translator()
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        input_str = (
            message.text.split(None, 1)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        target = input_str or "id"
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edit_or_reply(
                message,
                f"**ERROR:** __{str(err)}__",
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            return
    else:
        input_str = (
            message.text.split(None, 2)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        text = message.text.split(None, 2)[2]
        target = input_str or "id"
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edit_or_reply(
                message,
                "**ERROR:** __{}__".format(str(err)),
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            return
    await edit_or_reply(
        message,
        f"**Translated to:** __{target}__\n__{tekstr.text}__\n\n**Detected Language:** __{(await trl.detect(text))}__",
        parse_mode=enums.ParseMode.MARKDOWN,
    )


add_command_help(
    "translate",
    [
        [
            "tr <language code> <text/reply>",
            "Translates text to the set language. (Default is indonesian)",
        ],
    ],
)
