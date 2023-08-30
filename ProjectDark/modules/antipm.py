# Part of Dragon-Userbot


import asyncio

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from ProjectDark.helpers.basic import edit_or_reply

from ProjectDark.helpers.SQL.globals import addgvar, gvarstatus, CMD_HANDLER as cmd, ANTIPM
from ProjectDark.helpers.tools import get_arg
from .help import add_command_help

in_contact_list = filters.create(lambda _, __, message: message.from_user.is_contact)
is_support = filters.create(lambda _, __, message: message.chat.is_support)



@Client.on_message(filters.command("nopm", cmd) & filters.me)
async def set_nopm(client: Client, message: Message):
    nopm = get_arg(message)
    status_nopm = gvarstatus("ANTIPM")
    if not nopm:
        return await edit_or_reply(message, f"Currently nopm is `{status_nopm}`")
    if nopm not in ["on", "off"]:
        return await edit_or_reply(message, "Invalid!")
    else:
        addgvar("ANTIPM", nopm)
        await message.edit(f"NoPM changed to `{nopm}`\nRestart userbot to take effect.")
        
@Client.on_message(
    filters.private
    & ~filters.me
    & ~filters.bot
    & ~in_contact_list
    & ~is_support
)
async def _antipm_handler(client: Client, message: Message):
    if not ANTIPM:
        return
    user_info = await client.resolve_peer(message.chat.id)
    msg = await client.send_message(
        message.chat.id,
        "PM w/o permission!"
        )
    for countdown in ["3", "2", "1"]:
        await asyncio.sleep(1)
        await msg.edit(countdown)
    
    await client.send(
        functions.messages.DeleteHistory(
        peer=user_info,
        max_id=0,
        revoke=True)
        )
        

add_command_help(
    "nopm",
    [
        ["nopm <on/off>",
        "If set `on`: Any message from stranger will be purged.",
        ],
    ],
)
        