import os
import sys
import traceback

from io import StringIO

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd

from .help import add_command_help


async def _exec(code, c, m, r, chat):
    m = m
    r = m.reply_to_message
    c = c
    chat = m.chat
    exec(
        f"async def _aexec(c, m, r, chat): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["_aexec"](c, m, r, chat)


@Client.on_message(filters.command("ev", cmd) & filters.me)
async def evaluate(c: Client, m: Message):
    msg = await m.edit("Processing...")
    try:
        code = m.text.split(maxsplit=1)[1]
    except IndexError:
        await msg.edit("Invalid!")
        return
    reply_to_id = m.id
    r = m.reply_to_message
    chat = m.chat
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await _exec(code, c, m, r, chat)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success!"
    final = f"<code>{code}</code>\n\nOutput:\n<code>{evaluation.strip()}</code>"
    if len(final) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final))
        await m.reply_document(
            document=filename,
            caption=code,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await m.delete()
    else:
        await msg.edit(final)



add_command_help(
    "python",
    [
        ["ev",
        "Evaluate code.",
        ],
    ],
)