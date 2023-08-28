# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import html

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.parser import mention_html, mention_markdown
from ProjectDark.modules.help import *


@Client.on_message(filters.me & filters.command("admins", cmd))
async def adminlist(client: Client, message: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    creator = []
    admin = []
    badmin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        try:
            name = a.user.first_name + " " + a.user.last_name
        except:
            name = a.user.first_name
        if name is None:
            name = "No Name"
        if a.status == enums.ChatMemberStatus.ADMINISTRATOR:
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, name))
            else:
                admin.append(mention_markdown(a.user.id, name))
        elif a.status == enums.ChatMemberStatus.OWNER:
            creator.append(mention_markdown(a.user.id, name))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = "Admins in {}\n".format(grup.title)
    teks += "Creator: "
    for x in creator:
        teks += "{}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "\n{} total admins\n".format(len(admin))
    for x in admin:
        teks += "{}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "\n{} bot admins\n".format(len(badmin))
    for x in badmin:
        teks += "{}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "\nTotal: {} admins".format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)


@Client.on_message(filters.me & filters.command("bots", cmd))
async def get_list_bots(client: Client, message: Message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    getbots = client.get_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            name = a.user.first_name + " " + a.user.last_name
        except:
            name = a.user.first_name
        if name is None:
            name = "No Name"
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, name))
    teks = "All bots in group {}\n".format(grup.title)
    for x in bots:
        teks += "{}\n".format(x)
    teks += "\nTotal: {} bots".format(len(bots))
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)


add_command_help(
    "staff",
    [
        ["admins",
        "List admins in current chats."
        ],
        
        ["bots",
        "List bots in current chat.",
        ],
    ],
)
