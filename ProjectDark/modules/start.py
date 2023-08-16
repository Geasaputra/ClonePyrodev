# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from config import *
from ProjectDark import *
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.constants import First

from .help import add_command_help



@Client.on_message(filters.command("repo", cmd) & filters.me)
async def repo(client: Client, message: Message):
    await edit_or_reply(
        message, First.REPO.format(BOT_VER), disable_web_page_preview=True
    )


@Client.on_message(filters.command("creator", cmd) & filters.me)
async def creator(client: Client, message: Message):
    await edit_or_reply(message, First.CREATOR)


@Client.on_message(filters.command("uptime", cmd) & filters.me)
async def uptime(client: Client, message: Message):
    now = datetime.now()
    current_uptime = now - START_TIME
    await edit_or_reply(
        message, f"Uptime: {str(current_uptime).split('.')[0]}"
    )


@Client.on_message(filters.command("id", cmd) & filters.me)
async def get_id(client: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"ID: `{rep.audio.file_id}`\n"
            file_id += "Type: `Audio`"

        elif rep.document:
            file_id = f"ID:`{rep.document.file_id}`\n"
            file_id += f"Type: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"ID: `{rep.photo.file_id}`\n"
            file_id += "Type: `Photo`"

        elif rep.sticker:
            file_id = f"ID: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"Set: `{rep.sticker.set_name}`\n"
                file_id += f"Emoji: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"Sticker: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "Animated: `False`\n"
            else:
                file_id += "Sticker: `None`\n"
                file_id += "Emoji: `None`"

        elif rep.video:
            file_id = f"ID: `{rep.video.file_id}`\n"
            file_id += "Type: `Video`"

        elif rep.animation:
            file_id = f"ID: `{rep.animation.file_id}`\n"
            file_id += "Type: `GIF`"

        elif rep.voice:
            file_id = f"ID: `{rep.voice.file_id}`\n"
            file_id += "Type: `Voice Note`"

        elif rep.video_note:
            file_id = f"ID: `{rep.animation.file_id}`\n"
            file_id += "Type: `Video Note`"

        elif rep.location:
            file_id = "Location\n"
            file_id += f"Longitude: `{rep.location.longitude}`\n"
            file_id += f"Latitude: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "Location\n"
            file_id += f"Longitude: `{rep.venue.location.longitude}`\n"
            file_id += f"Latitude: `{rep.venue.location.latitude}`\n\n"
            file_id += "Address\n"
            file_id += f"Title: `{rep.venue.title}`\n"
            file_id += f"Detailed: `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = f"Forwarded: `{message.reply_to_message.forward_from.id}`\n"
        else:
            user_detail = (
                f"From: `{message.reply_to_message.from_user.id}`\n"
            )
        user_detail += f"Message: `{message.reply_to_message.id}`"
        await message.edit(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = f"Forwarded: `{message.reply_to_message.forward_from.id}`\n"
        else:
            user_detail = (
                f"From: `{message.reply_to_message.from_user.id}`\n"
            )
        user_detail += f"Message: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        await edit_or_reply(message, user_detail)

    else:
        await edit_or_reply(message, f"Chat: `{message.chat.id}`")


# Command help section
add_command_help(
    "start",
    [
        ["alive",
        "Just for fun."
        ],
        
        ["repo",
        "Display the repo of this userbot."
        ],
        
        ["creator",
        "Show the creator of this userbot."
        ],
        
        ["id",
        "Send id of what you replied to."
        ],
        
        ["uptime",
        "Check bot's current uptime."
        ],
    ],
)
