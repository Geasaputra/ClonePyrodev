# Part of Dragon-Userbot


import asyncio

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from ProjectDark.helpers.SQL.globals import addgvar, gvarstatus
from ProjectDark.helpers.tools import get_arg


in_contact_list = filters.create(lambda _, __, message: message.from_user.is_contact)
is_support = filters.create(lambda _, __, message: message.chat.is_support)


@Client.on_message(filters.command("antipm", cmd) & filters.me)
async def _antipm(client: Client, message: Message):
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
        
    if gvarstatus("ANTIPM") and gvarstatus("ANTIPM") == "false":
        ANTIPM = False
    else:
        ANTIPM = True
        
    if ANTIPM:
        if h_type:
            await edit_or_reply(message, "Anti-PM activated!")
        else:
            addgvar("ANTIPM", h_type)
            await edit_or_reply(message, "Anti-PM deactivated!")
            
    elif h_type:
        addgvar("ANTIPM", h_type)
        await edit_or_reply(message, "Anti-PM activated!")
    else:
        await edit_or_reply(message, "Anti-PM deactivated!")


@Client.on_message(
    filters.private
    & ~filters.me
    & ~filters.bot
    & ~in_contact_list
    & ~is_support
)
async def _antipm_handler(client: Client, message: Message):
    if gvarstatus("ANTIPM") and gvarstatus("ANTIPM") == "false":
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
        