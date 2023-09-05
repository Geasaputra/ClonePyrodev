from asyncio import sleep

from pyrogram import Client, filters

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd, BOTLOG_CHATID as log
from ProjectDark.helpers.SQL.notes_sql import add_note, get_note, get_notes, rm_note
from ProjectDark.helpers.tools import get_arg
from ProjectDark.modules.help import add_command_help


@Client.on_message(filters.command("notes", cmd) & filters.me)
async def _notes(client, message):
    user_id = message.from_user.id
    notes = get_notes(str(user_id))
    if not notes:
        return await message.reply("No notes are found!")
    
    msg = "List Saved Notes:\n"
    for note in notes:
        msg += f"`{note.keyword}`\n"
    await message.edit(msg)


@Client.on_message(filters.command("clear", cmd) & filters.me)
async def rmnote(client, message):
    notename = get_arg(message)
    user_id = message.from_user.id
    if rm_note(str(user_id), notename) is False:
        return await message.reply(
            "No found notes for `{}`.".format(notename)
        )
    return await message.reply(
        "Successfully remove note: `{}`".format(notename)
    )


@Client.on_message(filters.command("save", cmd) & filters.me)
async def addnote(client, message):
    keyword = get_arg(message)
    user_id = message.from_user.id
    msg = message.reply_to_message
    if not msg:
        return await message.reply("Reply to message!")
    fwd = await msg.forward(log)
    msg_id = fwd.id
    await client.send_message(
        log,
        f"#NOTE\nKeyword: `{keyword}`"
    )
    await sleep(2)
    add_note(str(user_id), keyword, msg_id)
    await message.edit(f"Successfully save note: `{keyword}`")


@Client.on_message(filters.command("get", cmd) & filters.me)
async def _note(client, message):
    notename = get_arg(message)
    user_id = message.from_user.id
    note = get_note(str(user_id), notename)
    if not note:
        return await message.reply("No notes are found!")
    msg_o = await client.get_messages(log, int(note.f_mesg_id))
    await message.delete()
    await msg_o.copy(message.chat.id, reply_to_message_id=message.id)


add_command_help(
    "notes",
    [
        ["notes",
        "List all notes are available.",
        ],
        
        ["save",
        "Save to notes.",
        ],
        
        ["clear",
        "Remove from notes.",
        ],
        
        ["get",
        "Get notes.",
        ],
    ],
)

