# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
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
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    admin = ubot.can_change_info
    member = message.chat.permissions.can_change_info
    if not (admin or member):
        await message.edit_text("No permissions!")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("Reply to a photo!")


@Client.on_message(filters.group & filters.command("ban", cmd) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    msg = await edit_or_reply(message, "Processing...")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_restrict_members:
        return await msg.edit("No permissions!")
    if not user_id:
        return await msg.edit("Not found!")
    if user_id == client.me.id:
        return await msg.edit("No right!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await msg.edit("Not right!")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msgs = (
        f"{mention} banned by {message.from_user.mention if message.from_user else 'Anonymous'}!\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msgs += f"Reason: {reason}"
    await message.chat.ban_member(user_id)
    await msg.edit(msgs)


@Client.on_message(filters.group & filters.command("unban", cmd) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    msg = await edit_or_reply(message, "Processing...")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_restrict_members:
        return await msg.edit("No permissions!")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await msg.edit("No right!")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await msg.edit("Username/ID or reply to user!")
    await message.chat.unban_member(user)
    umention = (await cleint.get_users(user)).mention
    await msg.edit(f"{umention} unbanned!")


@Client.on_message(filters.command("pin", cmd) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await edit_or_reply(message, "Reply to message!")
    msg = await edit_or_reply(message, "Processing...")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_pin_messages:
        return await msg.edit("No permissions!")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await msg.edit(
            f"[Unpinned]({r.link})!",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await msg.edit(
        f"[Pinned]({r.link})!",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("mute", cmd) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    msg = await edit_or_reply(message, "Processing...")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_restrict_members:
        return await msg.edit("No permissions!")
    if not user_id:
        return await msg.edit("Not found!")
    if user_id == client.me.id:
        return await msg.edit("No right!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await msg.edit("No right!")
    mention = (await client.get_users(user_id)).mention
    msgs = (
        f"{mention} muted by {message.from_user.mention if message.from_user else 'Anonymous'}!\n"
    )
    if reason:
        msgs += f"Reason: {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await msg.edit(msgs)


@Client.on_message(filters.group & filters.command("unmute", cmd) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    msg = await edit_or_reply(message, "Processing...")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_restrict_members:
        return await msg.edit("No permissions!")
    if not user_id:
        return await msg.edit("Not found!")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await msg.edit(f"{umention} unmuted!")


@Client.on_message(filters.command("kick", cmd) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    msg = await edit_or_reply(message, "Processing...")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_restrict_members:
        return await msg.edit("No permission!")
    if not user_id:
        return await msg.edit("Not found!")
    if user_id == client.me.id:
        return await msg.edit("No right!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await msg.edit("No right!")
    mention = (await client.get_users(user_id)).mention
    msgs = f"{mention} kicked by {message.from_user.mention if message.from_user else 'Anonymous'}!"
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msgs += f"\nReason: {reason}"
    try:
        await message.chat.ban_member(user_id)
        await msg.edit(msgs)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await msg.edit("No permissions!")


@Client.on_message(filters.group & filters.command(["promote", "fpromote"], cmd) & filters.me)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    msg = await edit_or_reply(message, "Processing...")
    if not user_id:
        return await msg.edit("Not found!")
    ubot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not ubot.can_promote_members:
        return await msg.edit("No permissions!")
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
        return await msg.edit(f"{umention} fully promoted!")

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
    await msg.edit(f"{umention} promoted!")


@Client.on_message(filters.group & filters.command("demote", cmd) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    msg = await edit_or_reply(message, "Processing...")
    if not user_id:
        return await msg.edit("Not found!")
    if user_id == client.me.id:
        return await msg.edit("No right!")
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
    await msg.edit(f"{umention} demoted!")


add_command_help(
    "admins",
    [
        ["ban <reply or id/username> <reason>",
        "Ban user from your group."
        ],
        
        ["unban <reply or id/username> <reason>",
        "Unban user from your group.",
        ],
        
        ["kick <reply or id/username> <rreason>",
        "Kick user from your group."
        ],
        
        ["promote or fullpromote",
        "Promote user from your group.",
        ],
        
        ["demote",
        "Demote user from your group."
        ],
        
        ["mute <reply or id/usernmae>",
        "Mute user from your group.",
        ],
        
        [f"unmute <reply or id/username>",
        "Unmute user from your group.",
        ],
        
        ["pin <reply to message>",
        "Pin a message on your group.",
        ],
        
        ["unpin <reply to message>",
        "Unpin a message on your group.",
        ],
        
        ["gpic <reply to photo>",
        "Change group pic.",
        ],
    ],
)