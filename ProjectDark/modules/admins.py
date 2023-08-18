# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions import bad_request_400
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.modules.help import add_command_help
from ProjectDark.utils.misc import extract_user, extract_user_and_reason, list_admins

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(
    filters.group & filters.command("gpic", cmd) & filters.me
)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("Don't have enough permission!")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("Reply to a photo to set it!")


@Client.on_message(filters.command("gname", cmd) & filters.me)
async def set_chat_tittle(client: Client, message: Message):
    if message.chat.type == enums.ChatType.GROUP or message.chat.type == enums.ChatType.SUPERGROUP or message.chat.type == enums.ChatType.CHANNEL:
        if len(message.command) == 1:
            if message.reply_to_message:
                if message.reply_to_message.text:
                    try:
                        await client.set_chat_title(chat_id=message.chat.id, title=message.reply_to_message.text)
                    except bad_request_400.ChatAdminRequired:
                        await message.reply("Admin reuired!")
                    except bad_request_400.ChatNotModified:
                        await message.reply("Nothing has change!")
                    except Exception as e:
                        print(e)
                        await message.reply("Can't change tittle!")
                elif message.reply_to_message.caption:
                    try:
                        await client.set_chat_title(chat_id=message.chat.id, title=message.reply_to_message.caption)
                    except bad_request_400.ChatAdminRequired:
                        await message.reply("Admin reuired!")
                    except bad_request_400.ChatNotModified:
                        await message.reply("Nothing has change!")
                    except Exception as e:
                        print(e)
                        await message.reply("Can't set tittle!")
                else:
                    await message.reply("No text in message!")
            else:
                await message.reply("See `.help admins`", parse_mode=enums.ParseMode.MARKDOWN)

        elif len(message.command) >= 2:
            try:
                await client.set_chat_title(chat_id=message.chat.id,
                title=message.text[3+1:])
            except bad_request_400.ChatAdminRequired:
                await message.reply("Admin required!")
            except bad_request_400.ChatNotModified:
                await message.reply("Nothing has changed!")
            except Exception as e:
                print(e)
                await message.reply("Can't set tittle!")
      
    else:
        await message.reply("Only for channel/group!")
  

@Client.on_message(filters.group & filters.command("ban", cmd) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    Dark = await edit_or_reply(message, "Processing...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Dark.edit("Not have enough permissions!")
    if not user_id:
        return await Dark.edit("Can't find that user!")
    if user_id == client.me.id:
        return await Dark.edit("Can't ban your self!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Dark.edit("Can't ban Admins!")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"{mention} banned!\n"
        f"Banned by {message.from_user.mention if message.from_user else 'Anonymous'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"Reason: {reason}"
    await message.chat.ban_member(user_id)
    await Dark.edit(msg)


@Client.on_message(filters.group & filters.command("unban", cmd) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    Dark = await edit_or_reply(message, "Processing...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Dark.edit("Not have enough permissions!")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await Dark.edit("Can't unban channel!")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await Dark.edit(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await Dark.edit(f"{umention} unbanned!")


@Client.on_message(filters.command(["pin", "unpin"], cmd) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await edit_or_reply(message, "Reply to a message to pin/unpin it!")
    Dark = await edit_or_reply(message, "Processing...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await Dark.edit("Not have enough permissions!")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await Dark.edit(
            f"[Message]({r.link}) unpinned!",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await Dark.edit(
        f"[Message]({r.link}) pinned!",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("unpinall", cmd) & filters.me)
async def unpinall(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Processing...")
    privileges = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not privileges.can_pin_messages:
        return await Dark.edit("Not have enough permissions!")
    else:
        chat_id  = message.chat.id
        await client.unpin_all_chat_messages(chat_id)
        return await Dark.edit("All messages unpinned!")
        



@Client.on_message(filters.command("mute", cmd) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    Dark = await edit_or_reply(message, "Processing...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Dark.edit("Not have enough permissions!")
    if not user_id:
        return await Dark.edit("Can't find that user!")
    if user_id == client.me.id:
        return await Dark.edit("Can't mute your self!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Dark.edit("Can't mute admin!")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"{mention} muted!\n"
        f"Muted by {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"Reason: {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await Dark.edit(msg)


@Client.on_message(filters.group & filters.command("unmute", cmd) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    Dark = await edit_or_reply(message, "Processing...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Dark.edit("Not have enough permissions!")
    if not user_id:
        return await Dark.edit("Can't find that user!")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await Dark.edit(f"{umention} unmuted!")


@Client.on_message(filters.command(["kick", "dkick"], cmd) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    Dark = await edit_or_reply(message, "Processing...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Dark.edit("Not have enough permissions!")
    if not user_id:
        return await Dark.edit("Can't find that user!")
    if user_id == client.me.id:
        return await Dark.edit("Can't kick your self!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Dark.edit("Can't kick Admins!")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
{mention} kicked!
Kicked by {message.from_user.mention if message.from_user else 'Anon'}
"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\nReason: {reason}"
    try:
        await message.chat.ban_member(user_id)
        await Dark.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await Dark.edit("You are not admin!")


@Client.on_message(
    filters.group & filters.command(["promote", "fpromote"], cmd) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    Dark = await edit_or_reply(message, "Processing...")
    if not user_id:
        return await Dark.edit("Can't find that user!")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await Dark.edit("Not have enough permissions!")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await Dark.edit(f"{umention} fully promoted!")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await Dark.edit(f"{umention} promoted!")


@Client.on_message(filters.group & filters.command("demote", cmd) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    Dark = await edit_or_reply(message, "Processing...")
    if not user_id:
        return await Dark.edit("Can't find that user!")
    if user_id == client.me.id:
        return await Dark.edit("Can't demote your self!")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await Dark.edit(f"{umention} demoted!")


add_command_help(
    "admins",
    [
        ["ban <reply/username/userid> <reason>",
        "Ban a user from your group"
        ],
        
        ["unban <reply/username/userid> <reason>", "Unban a user from your group.",
        ],
        
        ["kick <reply/username/userid>",
        "Kick a user from your group."
        ],
        
        ["dkick <reply/username/userid>",
        "Kick a user from your group and delete message."
        ],
        
        ["promote",
        "Promote a user from your group.",
        ],
        
        ["fpromote",
        "Fully promote a user from your group.",
        ],
        
        ["demote",
        "Demote a user from your group."
        ],
        
        ["mute <reply/username/userid>",
        "Mute a user from your group",
        ],
        
        ["unmute <reply/username/userid>",
        "Unmute a user from your group.",
        ],
        
        ["pin <reply to message>",
        "Pinned a message.",
        ],
        
        ["unpin <reply to message>",
        "Unpin a message.",
        ],
        
        ["unpinall",
        "Unpin all messages.",
        ],
        
        ["gpic <reply to photo>",
        "Set a profile picture for your group.",
        ],
        
        ["gname <text/reply to text>",
        "Set a new tittle for your group.",
        ],
    ],
)
