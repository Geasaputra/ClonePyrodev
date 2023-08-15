# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.command("join", cmd) & filters.me)
async def join(client: Client, message: Message):
    Dark = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "Joining to chat...")
    try:
        await xxnx.edit(f"Successfully joined!\nChat ID: `{Dark}`")
        await client.join_chat(Dark)
    except Exception as ex:
        await xxnx.edit(f"{str(ex)}")


@Client.on_message(filters.command(["leave", "kickme"], cmd) & filters.me)
async def leave(client: Client, message: Message):
    Dark = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "Good bye!")
    try:
        await xxnx.edit_text(f"{client.me.first_name} has left.")
        await client.leave_chat(Dark)
    except Exception as ex:
        await xxnx.edit_text(f"{str(ex)}")


@Client.on_message(filters.command(["leaveallgc"], cmd) & filters.me)
async def kickmeall(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Leaving all groups...")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Dark.edit(
        f"Successfully leave all groups!\nDone: {done}\nFailed: {er}"
    )


@Client.on_message(filters.command(["leaveallch"], cmd) & filters.me)
async def kickmeallch(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Leaving from all channels...")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Dark.edit(
        f"Successfully leave from all channels!\nDone: {done}\nFailed: {er}"
    )


add_command_help(
    "joinleave",
    [
        ["kickme",
        "Leave from currently group.",
        ],
        
        ["leaveallgc",
        "Leave from all groups you have joined."
        ],
        
        ["leaveallch",
        "Leave all channels you have joined."
        ],
        
        ["join <username>",
        "Join group chat with the username."
        ],
        
        ["leave <UsernameGC>",
        "Leav group chat with the username."
        ],
    ],
)
