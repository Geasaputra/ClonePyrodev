# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from asyncio import gather
from os import remove

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.PyroHelpers import ReplyCheck
from ProjectDark.utils import extract_user

from .help import add_command_help


@Client.on_message(filters.command("info", cmd) & filters.me)
async def who_is(client: Client, message: Message):
    user_id = await extract_user(message)
    Dark = await edit_or_reply(message, "Processing...")
    if not user_id:
        return await Dark.edit(
            "Invalid!"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""
<a href='tg://user?id={user.id}'><b>User Information</b></a>

User ID: <code>{user.id}</code>
First Name: {first_name}
Last Name: {last_name}
Last Seen: {status}
Username: {username}
Bio:
{bio}

Data Center: {dc_id}
Verified: {user.is_verified}
Premium: {user.is_premium}
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Dark.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await Dark.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Dark.edit(f"{e}")


@Client.on_message(filters.command("cinfo", cmd) & filters.me)
async def chatinfo_handler(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Processing...")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.edit(
                    f"`{cmd}chatinfo` <group username/id>"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""
<b>{chat.title}</b> ({type})
Total {chat.members_count} members

Username: {username}
ID: <code>{chat.id}</code>
DC: {dc_id}

Verified: {chat.is_verified}
Restricted: {chat.is_restricted}
Protected: {chat.has_protected_content}

Description:
{description}
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Dark.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await Dark.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Dark.edit(f"{e}")


add_command_help(
    "info",
    [
        ["info <username/userid/reply>",
        "Get telegram user info with full description.",
        ],
        
        ["cinfo <username/chatid>",
        "Get group info with full description.",
        ],
    ],
)
