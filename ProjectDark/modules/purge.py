# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.command("del", cmd) & filters.me)
async def del_msg(client: Client, message: Message):
    msg_src = message.reply_to_message
    if msg_src:
        if msg_src.from_user.id:
            try:
                await client.delete_messages(message.chat.id, msg_src.id)
                await message.delete()
            except BaseException:
                pass
    else:
        await message.delete()


@Client.on_message(filters.command("purge", cmd) & filters.me)
async def purge(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Starting to purge messages!")
    msg = message.reply_to_message
    if msg:
        itermsg = list(range(msg.id, message.id))
    else:
        await Dark.edit("Reply to message to purge!")
        return
    count = 0

    for i in itermsg:
        try:
            count = count + 1
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=i, revoke=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await Dark.edit(f"{e}")
            return

    done = await Dark.edit(
        f"{str(count)} messages are purged!"
    )
    await asyncio.sleep(2)
    await done.delete()


@Client.on_message(filters.command("purgeme", cmd) & filters.me)
async def purge_me(client, message):
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply("Invalid!")
    n = int(n)
    if n < 1:
        return await message.reply("Need count >=1-999")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await eor(message, text="No messages are found!")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
        dark = await message.reply(f"{n} your messages are purged!")
        await asyncio.sleep(1)
        await dark.delete()


add_command_help(
    "purge",
    [
        ["del",
        "Reply to message you want to delete."
        ],
        
        ["purge",
        "Clean message from you replied messages."
        ],
        
        ["purgeme <amounts>",
        "Prune only your messages."],
    ],
)
