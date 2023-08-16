# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType #, UserStatus
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import BOTLOG_CHATID
from ProjectDark.helpers.basic import edit_or_reply

from .help import *


@Client.on_message(filters.me & filters.command("invite", cmd))
async def inviteee(client: Client, message: Message):
    mg = await edit_or_reply(message, "Inviting user...")
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("Give user to add!")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"Unable to invite user! \n{e}")
        return
    await mg.edit(f"{len(user_list)} invited!")


@Client.on_message(filters.command("invitelink", cmd) & filters.me)
async def invite_link(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Processing...")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await Dark.edit(f"Link: {link}")
        except Exception:
            await Dark.edit("No permission!")


add_command_help(
    "invite",
    [
        ["invitelink",
        "Get invite link your group.",
        ],
        
        ["invite user1 user2 ...",
        "Invite a user or some users."
        ],
    ],
)
