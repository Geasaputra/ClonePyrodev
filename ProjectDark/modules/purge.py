import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd

from .help import add_command_help

async def purge_messages(
    client: Client,
    message: Message,
    start: int = 0,
    end: int = 0,
    type: str = "all",
    count: int = 0,
) -> None:
    count_deleted = 0
    index = 0
    while (count_deleted < count) if not count == 0 else (start + index < end):
        try:
            m = await client.get_messages(
                chat_id=message.chat.id,
                message_ids=(start - index) if not count == 0 else (start + index),
                replies=0,
            )
            if m:
                if type == "me":
                    if not m.from_user.id == message.from_user.id:
                        index += 1
                        continue
                if await m.delete():
                    count_deleted += 1
        except:
            pass
        index += 1
    if count_deleted > 0:
        m = await message.reply(
            text=f"{count_deleted} messages are purged")
        await asyncio.sleep(1)
        await m.delete()
    return [True, count_deleted]


@Client.on_message(filters.command("del", cmd) & filters.me)
async def _del(client: Client, message: Message) -> None:
    await message.delete()
    if message.reply_to_message:
        try:
            m = await client.get_messages(
                chat_id=message.chat.id, message_ids=message.reply_to_message.id, replies=0
            )
            await m.delete()
        except:
            pass


@Client.on_message(filters.command("purge", cmd) & filters.me)
async def _purge(client: Client, message: Message) -> None:
    await message.delete()
    if message.reply_to_message:
        await purge_messages(client, message,
        start=message.reply_to_message.id, end=message.id)

@Client.on_message(filters.command("purgeme", cmd) & filters.me)
async def _purgeme(client: Client, message: Message) -> None:
    await message.delete()

    count = int(message.command[1]) if len(message.command) > 1 else 1
    if message.reply_to_message:
        await purge_messages(client, message, start=message.reply_to_message.id, type="me", count=count)
    else:
        await purge_messages(client, message, start=message.id - 1, type="me", count=count)

add_command_help(
    "purge",
    [
        ["del",
        "Reply to message you want to delete."
        ],
        
        ["purge",
        "Clean message from you replied messages."
        ],
        
        ["purgeme <count>",
        "Prune only your messages."],
    ],
)
