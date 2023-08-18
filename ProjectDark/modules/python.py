import traceback
import os

from io import StringIO
from contextlib import redirect_stdout

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd

from .help import add_command_help


@Client.on_message(filters.command("ex", cmd) & filters.me)
async def execute(client: Client, message: Message):
    try:
        if len(message.command) == 1:
            await message.edit("Code to execute isn't provided!")
            return

        reply = message.reply_to_message
        code = message.text.split(maxsplit=1)[1]
        stdout = StringIO()

        await message.edit("Executing...")

        with redirect_stdout(stdout):
            exec(code)
        result = stdout.getvalue()

        if len(result) <= 4096:
            text = (
                f"<code>{code}</code>\n\n"
                "Result:\n"
                f"<code>{result}</code>"
            )
            await message.edit(text)
        else:
            with open("result.txt", "w") as file:
                file.write(result)

            await message.reply_document(document="result.txt")

            os.remove("result.txt")

    except Exception as e:
        error_message = f"<code>{traceback.format_exc()}</code>"
        await message.edit(error_message)


add_command_help(
    "python",
    [
        [f"ex or {cmd}exec <python code>",
        "Execute python code.",
        ],
    ],
)